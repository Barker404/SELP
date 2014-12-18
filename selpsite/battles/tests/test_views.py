from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from battles.models import Move, Player, Battle
from battles.views import joinBattle, chooseMove, calculateTurn, calculateDamage

class BattlesViewsTestCase_Views(TestCase):
    fixtures = ['auth_user_testdata']

    # Tests the response from the battle view when the user is logged in
    def test_battle_view_auth(self):
        loggedIn = self.client.login(username='staff', password='staffPass')
        self.assertTrue(loggedIn)

        response = self.client.get(reverse('battle'))
        self.assertEqual(response.status_code, 200)

    # Tests the response from the battle view when the user is not 
    # logged in
    def test_battle_view_unauth(self):
        response = self.client.get(reverse('battle'))
        self.assertRedirects(response, r'/users/login/?next=/battle/', 
            status_code=302, target_status_code=200)


class BattlesViewsTestCase_Join(TestCase):
    fixtures = ['auth_user_testdata', 'battles_player_testdata']

    def setUp(self):
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='lewis')
        self.user3 = User.objects.get(username='staff')
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)

    # Tests joinBattle in the case where there are no existing battles 
    # and it creates a new one
    def test_join_battle_create(self):
        self.assertEqual(Battle.objects.count(), 0)
        success = joinBattle(self.player1)

        self.assertTrue(success)
        self.assertEqual(Battle.objects.count(), 1)
        battle = Battle.objects.first()
        self.assertEqual(battle.status, Battle.WAITING_FOR_PLAYER)
        self.assertEqual(battle.player1, self.player1)

    # Tests joinBattle in the case where there is an existing battle 
    # with a player 1 in it
    def test_join_battle_existing_one(self):
        Battle.objects.create(player1=self.player1)
        self.assertEqual(Battle.objects.count(), 1)
        success = joinBattle(self.player2)

        self.assertTrue(success)
        self.assertEqual(Battle.objects.count(), 1)
        battle = Battle.objects.first()
        self.assertEqual(battle.player1, self.player1)
        self.assertEqual(battle.player2, self.player2)
        self.assertEqual(battle.status, Battle.WAITING_FOR_CHOICE)

    # Tests joinBattle in the case where there is an existing battle 
    # with a player 2 in it
    def test_join_battle_existing_two(self):
        Battle.objects.create(player2=self.player2)
        self.assertEqual(Battle.objects.count(), 1)
        success = joinBattle(self.player1)

        self.assertTrue(success)
        self.assertEqual(Battle.objects.count(), 1)
        battle = Battle.objects.first()
        self.assertEqual(battle.player2, self.player2)
        self.assertEqual(battle.player1, self.player1)
        self.assertEqual(battle.status, Battle.WAITING_FOR_CHOICE)

class BattlesViewsTestCase_Turns(TestCase):
    fixtures = ['auth_user_testdata',
                'users_testdata', 
                'battles_player_opponents_testdata', 
                'battles_battle_testdata', 
                'battles_move_testdata']

    def setUp(self):
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='lewis')
        self.user3 = User.objects.get(username='staff')
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.battle1 = Battle.objects.first()
        self.move1 = Move.objects.all()[0] # player1 - MR
        self.move2 = Move.objects.all()[1] # player2 - LR
        self.move3 = Move.objects.all()[2] # player1 - MC
        self.move4 = Move.objects.all()[3] # player1 - MA

    # Tests chooseMove in the case where the player is not in a battle
    def test_choose_move_bad_player(self):
        self.assertEqual(self.player3.move_set.count(), 0)
        success = chooseMove(self.player3, Move.SHORT_RANGE)
        self.assertFalse(success)
        self.assertEqual(self.player3.move_set.count(), 0)

    # Tests chooseMove in the case where the player's game does not 
    # have the correct status (WAITING_FOR_CHOICE) 
    def test_choose_move_bad_game(self):
        self.battle1.status = Battle.FINISHED
        self.battle1.save()
        self.assertEqual(self.player2.move_set.count(), 1)
        success = chooseMove(self.player2, Move.SHORT_RANGE)
        self.assertFalse(success)
        self.assertEqual(self.player2.move_set.count(), 1)
        self.assertEqual(self.battle1.status, Battle.FINISHED)

    # Tests chooseMove in the case where the player's move choice is 
    # not a valid choice
    def test_choose_move_bad_choice(self):
        self.assertEqual(self.battle1.turnNumber, 1)
        self.assertEqual(self.player1.move_set.count(), 3)
        success = chooseMove(self.player1, 'lol')
        self.assertFalse(success)
        self.assertEqual(self.player1.move_set.count(), 3)
        self.assertEqual(self.battle1.turnNumber, 1)

    # Tests chooseMove in the case where the player's move choice is 
    # valid - the good case
    def test_choose_move_good(self):
        self.assertEqual(self.battle1.turnNumber, 1)
        self.assertEqual(self.player1.move_set.count(), 3)
        success = chooseMove(self.player1, Move.SHORT_RANGE)
        self.assertTrue(success)
        self.assertEqual(self.player1.move_set.count(), 4)
        
        move = self.player1.move_set.last()
        self.assertEqual(move.player, self.player1)
        self.assertEqual(move.moveNo, 1)
        self.assertEqual(move.moveUsed, Move.SHORT_RANGE) 

    # Tests calculateDamage using various moves and distances
    def test_calculate_damage(self):
        distance = Battle.MEDIUM
        move = Move.MID_RANGE
        damage = calculateDamage(distance, move)
        self.assertEqual(damage, 30)

        distance = Battle.LONG
        move = Move.SHORT_RANGE
        damage = calculateDamage(distance, move)
        self.assertEqual(damage, 0)

        distance = Battle.SHORT
        move = Move.MOVE_CLOSE
        damage = calculateDamage(distance, move)
        self.assertEqual(damage, 0)

    # Tests calculateTurn in the case where player 1 for the battle 
    # is None
    def test_calculate_turn_bad_player1_none(self):
        self.player1.currentMove = self.move1
        self.player1.save()
        self.player2.currentMove = self.move2
        self.player2.save()
        self.battle1.status = Battle.CALCULATING
        self.battle1.save()

        self.calculate_turn_sanity()

        self.battle1.player1 = None
        self.battle1.save()
        success = calculateTurn(self.battle1)
        self.assertFalse(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.calculate_turn_sanity()

    # Tests calculateTurn in the case where player 2 for the battle 
    # is None
    def test_calculate_turn_bad_player2_none(self):
        self.player1.currentMove = self.move1
        self.player1.save()
        self.player2.currentMove = self.move2
        self.player2.save()
        self.battle1.status = Battle.CALCULATING
        self.battle1.save()

        self.battle1.player2 = None
        self.battle1.save()
        success = calculateTurn(self.battle1)
        self.assertFalse(success)
        
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.calculate_turn_sanity()

    # Tests calculateTurn in the case where the current move for 
    # player 1 is None
    def test_calculate_turn_bad_player1_current_move_none(self):
        self.player2.currentMove = self.move2
        self.player2.save()
        self.battle1.status = Battle.CALCULATING
        self.battle1.save()

        success = calculateTurn(self.battle1)
        self.assertFalse(success)
        
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.calculate_turn_sanity()

    # Tests calculateTurn in the case where the current move for 
    # player 2 is None
    def test_calculate_turn_bad_player2_current_move_none(self):
        self.player1.currentMove = self.move1
        self.player1.save()
        self.battle1.status = Battle.CALCULATING
        self.battle1.save()

        success = calculateTurn(self.battle1)
        self.assertFalse(success)
        
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.calculate_turn_sanity()

    # Tests calculateTurn in the case where the battle's status is 
    # not CALCULATING
    def test_calculate_turn_bad_status_wrong(self):
        self.player1.currentMove = self.move1
        self.player1.save()
        self.player2.currentMove = self.move2
        self.player2.save()

        self.battle1.status = Battle.WAITING_FOR_PLAYER
        self.battle1.save()
        success = calculateTurn(self.battle1)
        self.assertFalse(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.calculate_turn_sanity()
        
        self.battle1.status = Battle.WAITING_FOR_CHOICE
        self.battle1.save()
        success = calculateTurn(self.battle1)
        self.assertFalse(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.calculate_turn_sanity()

        self.battle1.status = Battle.FINISHED
        self.battle1.save()
        success = calculateTurn(self.battle1)
        self.assertFalse(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.calculate_turn_sanity()

    # Tests calculateTurn in the case where everything is correct
    # (but nobody wins or changes distance)
    def test_calculate_turn_good(self):
        self.player1.currentMove = self.move1
        self.player1.save()
        self.player2.currentMove = self.move2
        self.player2.save()
        self.battle1.status = Battle.CALCULATING
        self.battle1.save()

        self.calculate_turn_sanity()

        success = calculateTurn(self.battle1)
        self.assertTrue(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.assertEqual(self.battle1.status, Battle.WAITING_FOR_CHOICE)
        self.assertEqual(self.player1.currentMove, None)
        self.assertEqual(self.player2.currentMove, None)
        self.assertEqual(self.player1.lastMove, self.move1)
        self.assertEqual(self.player2.lastMove, self.move2)
        self.assertEqual(self.battle1.distance, Battle.MEDIUM)

        self.assertEqual(self.player1.hp, 80)
        self.assertEqual(self.player2.hp, 70)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 0)
        self.assertEqual(self.player2.user.profile.wins, 0)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 2)
        self.assertEqual(self.battle1.distance, Battle.MEDIUM)

    # Tests calculate turn in the case where everything is correct
    # and player 1 wins
    def test_calculate_turn_p1_wins(self):
        self.player1.currentMove = self.move1
        self.player1.hp = 20
        self.player1.save()
        self.player2.currentMove = self.move2
        self.player2.save()
        self.battle1.status = Battle.CALCULATING
        self.battle1.player1 = self.player2
        self.battle1.player2 = self.player1
        self.battle1.save()

        self.assertEqual(self.player1.hp, 20)
        self.assertEqual(self.player2.hp, 100)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 0)
        self.assertEqual(self.player2.user.profile.wins, 0)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 1)
        self.assertEqual(self.battle1.distance, Battle.MEDIUM)

        success = calculateTurn(self.battle1)
        self.assertTrue(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.assertEqual(self.battle1.status, Battle.FINISHED)
        self.assertEqual(self.battle1.winner, self.player2)
        self.assertEqual(self.player1.currentMove, self.move1)
        self.assertEqual(self.player2.currentMove, self.move2)

        self.assertEqual(self.player1.hp, 0)
        self.assertEqual(self.player2.hp, 70)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 1)
        self.assertEqual(self.player2.user.profile.wins, 1)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 1)
        self.assertEqual(self.battle1.distance, Battle.MEDIUM)
    
    # Tests calculate turn in the case where everything is correct
    # and player 2 wins
    def test_calculate_turn_p2_wins(self):
        self.player1.currentMove = self.move1
        self.player1.hp = 20
        self.player1.save()
        self.player2.currentMove = self.move2
        self.player2.save()
        self.battle1.status = Battle.CALCULATING
        self.battle1.save()

        self.assertEqual(self.player1.hp, 20)
        self.assertEqual(self.player2.hp, 100)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 0)
        self.assertEqual(self.player2.user.profile.wins, 0)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 1)
        self.assertEqual(self.battle1.distance, Battle.MEDIUM)

        success = calculateTurn(self.battle1)
        self.assertTrue(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.assertEqual(self.battle1.status, Battle.FINISHED)
        self.assertEqual(self.battle1.winner, self.player2)
        self.assertEqual(self.player1.currentMove, self.move1)
        self.assertEqual(self.player2.currentMove, self.move2)

        self.assertEqual(self.player1.hp, 0)
        self.assertEqual(self.player2.hp, 70)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 1)
        self.assertEqual(self.player2.user.profile.wins, 1)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 1)
        self.assertEqual(self.battle1.distance, Battle.MEDIUM)

    # Tests calculate turn in the case where everything is correct
    # and a player moves closer, reducing the distance (and affecting 
    # the damage dealt)
    def test_calculate_turn_good_move_close(self):
        self.player1.currentMove = self.move3
        self.player1.save()
        self.player2.currentMove = self.move2
        self.player2.save()
        self.battle1.status = Battle.CALCULATING
        self.battle1.save()

        self.calculate_turn_sanity()

        success = calculateTurn(self.battle1)
        self.assertTrue(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.assertEqual(self.battle1.status, Battle.WAITING_FOR_CHOICE)
        self.assertEqual(self.player1.currentMove, None)
        self.assertEqual(self.player2.currentMove, None)
        self.assertEqual(self.player1.lastMove, self.move3)
        self.assertEqual(self.player2.lastMove, self.move2)
        self.assertEqual(self.battle1.distance, Battle.SHORT)

        self.assertEqual(self.player1.hp, 85)
        self.assertEqual(self.player2.hp, 100)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 0)
        self.assertEqual(self.player2.user.profile.wins, 0)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 2)

    # Tests calculate turn in the case where everything is correct
    # and a player moves away, increasing the distance (and affecting 
    # the damage dealt)
    def test_calculate_turn_good_move_away(self):
        self.player1.currentMove = self.move4
        self.player1.save()
        self.player2.currentMove = self.move2
        self.player2.save()
        self.battle1.status = Battle.CALCULATING
        self.battle1.save()

        self.calculate_turn_sanity()

        success = calculateTurn(self.battle1)
        self.assertTrue(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.assertEqual(self.battle1.status, Battle.WAITING_FOR_CHOICE)
        self.assertEqual(self.player1.currentMove, None)
        self.assertEqual(self.player2.currentMove, None)
        self.assertEqual(self.player1.lastMove, self.move4)
        self.assertEqual(self.player2.lastMove, self.move2)
        self.assertEqual(self.battle1.distance, Battle.LONG)

        self.assertEqual(self.player1.hp, 70)
        self.assertEqual(self.player2.hp, 100)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 0)
        self.assertEqual(self.player2.user.profile.wins, 0)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 2)


    # Helper function used to check that all values are what they 
    # should be at the start
    def calculate_turn_sanity(self):
        self.assertEqual(self.player1.hp, 100)
        self.assertEqual(self.player2.hp, 100)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 0)
        self.assertEqual(self.player2.user.profile.wins, 0)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 1)
        self.assertEqual(self.player1.lastMove, None)
        self.assertEqual(self.player2.lastMove, None)
        self.assertEqual(self.battle1.distance, 2)

class BattleAjaxViewsTestCase(TestCase):
    fixtures = ['auth_user_testdata',
                'users_testdata', 
                'battles_player_opponents_testdata', 
                'battles_battle_testdata', 
                'battles_move_testdata']

    def setUp(self):
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='lewis')
        self.user3 = User.objects.get(username='staff')
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.battle1 = Battle.objects.first()
        self.move1 = Move.objects.all()[0] # player1 - R
        self.move2 = Move.objects.all()[1] # player2 - P
              
    # Tests the gatBattle AJAX view in various cases where the 
    # request is not granted
    def test_ajax_get_battle_details_view_bad(self):
        # Not logged in
        response = self.client.get(reverse('getBattleDetails'))
        self.assertEqual(response.status_code, 403)
        
        loggedIn = self.client.login(username='staff', password='staffPass')
        self.assertTrue(loggedIn)
        
        # Post
        response = self.client.post(reverse('getBattleDetails'), {})
        self.assertEqual(response.status_code, 400)
        # No playerId given
        response = self.client.get(reverse('getBattleDetails'))
        self.assertEqual(response.status_code, 400)
        # playerID doesn't exist
        playerId = 4
        self.assertFalse(Player.objects.filter(pk=playerId).exists())
        response = self.client.get(
            "{url}?playerId={id}".format(url=reverse('getBattleDetails'),
                                         id=playerId))
        self.assertEqual(response.status_code, 404)
        # Not logged in as user of playerId
        playerId = self.player1.pk
        response = self.client.get(
            "{url}?playerId={id}".format(url=reverse('getBattleDetails'),
                                         id=playerId))
        self.assertEqual(response.status_code, 403)
        # Player is not in a battle
        playerId = self.player3.pk
        response = self.client.get(
            "{url}?playerId={id}".format(url=reverse('getBattleDetails'),
                                         id=playerId))
        self.assertEqual(response.status_code, 400)

    # Tests the gatBattle AJAX view in the case where the request is granted
    def test_ajax_get_battle_status_view_good(self):
        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)

        playerId = self.player1.pk
        response = self.client.get(
            "{url}?playerId={id}".format(url=reverse('getBattleDetails'),
                                         id=playerId))
        self.assertEqual(response.status_code, 200)
        
    # Tests the createPlayer AJAX view in various cases where the 
    # request is not granted
    def test_ajax_create_player_view_bad(self):
        players = Player.objects.count()

        # Not logged in
        response = self.client.post(reverse('createPlayer'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Player.objects.count(), players)
        
        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)
        
        # Get
        response = self.client.get(reverse('createPlayer'), {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Player.objects.count(), players)

    # Tests the createPlayer AJAX view in the case where the request is granted
    def test_ajax_create_player_view_good(self):
        players = Player.objects.count()

        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)

        response = self.client.post(reverse('createPlayer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.content), players + 1)
        self.assertEqual(Player.objects.count(), players + 1)

    # Tests the startBattle AJAX view in various cases where the 
    # request is not granted
    def test_ajax_start_battle_view_bad(self):
        # Not logged in
        response = self.client.post(reverse('startBattle'))
        self.assertEqual(response.status_code, 403)
        
        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)
        
        # Get
        response = self.client.post(reverse('startBattle'), {})
        self.assertEqual(response.status_code, 400)
        # No playerId given
        response = self.client.post(reverse('startBattle'))
        self.assertEqual(response.status_code, 400)
        # playerID doesn't exist
        playerId = 4
        self.assertFalse(Player.objects.filter(pk=playerId).exists())
        response = self.client.post(reverse('startBattle'), { 'playerId' : playerId })
        self.assertEqual(response.status_code, 404)
        # Not logged in as user of playerId
        playerId = self.player2.pk
        response = self.client.post(reverse('startBattle'), { 'playerId' : playerId })
        self.assertEqual(response.status_code, 403)
        # Player is already in a battle
        playerId = self.player1.pk
        response = self.client.post(reverse('startBattle'), { 'playerId' : playerId })
        self.assertEqual(response.status_code, 400)

    # Tests the startBattle AJAX view in the case where the request is granted
    def test_ajax_start_battle_view_good(self):
        # Will only respond with "failure" in cases where multiple players are trying
        # to create battles at once
        # So we only test success case for simplicity
        self.assertFalse(self.player3.isInBattle())
        battles = Battle.objects.count()

        loggedIn = self.client.login(username='staff', password='staffPass')
        self.assertTrue(loggedIn)

        playerId = self.player3.pk
        response = self.client.post(reverse('startBattle'), { 'playerId' : playerId })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")

        self.player3 = Player.objects.get(user=self.user3)

        self.assertTrue(self.player3.isInBattle())
        self.assertEqual(Battle.objects.count(), battles + 1)
        battle = self.player3.getBattle()
        onePlayer = (((battle.player1 is None) and (not battle.player2 is None)) or
                    ((not battle.player1 is None) and (battle.player2 is None)))
        self.assertTrue(onePlayer)

    # Tests the chooseMove AJAX view in various cases where the 
    # request is not granted
    def test_ajax_choose_move_view_bad(self):
        # Not logged in
        response = self.client.post(reverse('chooseMove'))
        self.assertEqual(response.status_code, 403)
        
        loggedIn = self.client.login(username='staff', password='staffPass')
        self.assertTrue(loggedIn)
        
        # Get
        response = self.client.get(reverse('chooseMove'), {})
        self.assertEqual(response.status_code, 400)
        # No playerId given
        response = self.client.post(reverse('chooseMove'), 
                                    { 'moveChoice' : Move.SHORT_RANGE })
        # No moveChoice given
        playerId = self.player3.pk
        response = self.client.post(reverse('chooseMove'), 
                                    { 'playerId' : playerId })
        self.assertEqual(response.status_code, 400)
        # moveChoice is invalid
        response = self.client.post(reverse('chooseMove'), 
                                    { 'playerId' : playerId,
                                    'moveChoice' : 'lol' })
        self.assertEqual(response.status_code, 400)
        # playerID doesn't exist
        playerId = 4
        self.assertFalse(Player.objects.filter(pk=playerId).exists())
        response = self.client.post(reverse('chooseMove'), 
                                    { 'playerId' : playerId,
                                    'moveChoice' : Move.SHORT_RANGE })
        self.assertEqual(response.status_code, 404)
        # Not logged in as user of playerId
        playerId = self.player2.pk
        response = self.client.post(reverse('chooseMove'), 
                                    { 'playerId' : playerId,
                                    'moveChoice' : Move.SHORT_RANGE })
        self.assertEqual(response.status_code, 403)
        # Player is not in a battle
        playerId = self.player3.pk
        response = self.client.post(reverse('chooseMove'), 
                                    { 'playerId' : playerId,
                                    'moveChoice' : Move.SHORT_RANGE })
        self.assertEqual(response.status_code, 400)

    # Tests the chooseMove AJAX view in the case where the request is granted
    def test_ajax_choose_move_view_good(self):
        # The details of the actual move creation are covered in other tests
        # Here, just test that the view gets to that point and creates a move
        self.assertTrue(self.player1.isInBattle())
        moves = Move.objects.count()
        lastMove = self.player1.currentMove
        turnNumber = self.player1.getBattle().turnNumber

        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)

        playerId = self.player1.pk
        response = self.client.post(reverse('chooseMove'), 
                                    { 'playerId' : playerId,
                                    'moveChoice' : Move.SHORT_RANGE })
        self.assertEqual(response.status_code, 200)

        self.player1 = Player.objects.get(user=self.user1)

        move = self.player1.currentMove
        self.assertNotEqual(move, lastMove)
        self.assertEqual(Move.objects.count(), moves + 1)
        self.assertEqual(move.player, self.player1)
        self.assertEqual(move.moveUsed, Move.SHORT_RANGE)
        self.assertEqual(move.moveNo, turnNumber)
