from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from battles.models import Move, Player, Battle
from battles.views import joinBattle, chooseMove, calculateTurn

class BattlesViewsTestCase_Views(TestCase):

    def test_battle_view(self):
        response = self.client.get(reverse('battle'))
        self.assertEqual(response.status_code, 200)


class BattlesViewsTestCase_Join(TestCase):
    fixtures = ['auth_user_testdata', 'battles_player_testdata']

    def setUp(self):
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='lewis')
        self.user3 = User.objects.get(username='staff')
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)

    def test_join_battle_create(self):
        self.assertEqual(Battle.objects.count(), 0)
        success = joinBattle(self.player1)

        self.assertTrue(success)
        self.assertEqual(Battle.objects.count(), 1)
        battle = Battle.objects.first()
        self.assertEqual(battle.status, Battle.WAITING_FOR_PLAYER)
        self.assertEqual(battle.player1, self.player1)

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
        self.move1 = Move.objects.all()[0] # player1 - R
        self.move2 = Move.objects.all()[1] # player2 - P

    def test_choose_move_bad_player(self):
        self.assertEqual(self.player3.move_set.count(), 0)
        success = chooseMove(self.player3, 'R')
        self.assertFalse(success)
        self.assertEqual(self.player3.move_set.count(), 0)

    def test_choose_move_bad_game(self):
        self.battle1.status = Battle.FINISHED
        self.battle1.save()
        self.assertEqual(self.player2.move_set.count(), 1)
        success = chooseMove(self.player2, 'R')
        self.assertFalse(success)
        self.assertEqual(self.player2.move_set.count(), 1)
        self.assertEqual(self.battle1.status, Battle.FINISHED)

    def test_choose_move_bad_choice(self):
        self.assertEqual(self.battle1.turnNumber, 1)
        self.assertEqual(self.player1.move_set.count(), 1)
        success = chooseMove(self.player1, 'lol')
        self.assertFalse(success)
        self.assertEqual(self.player1.move_set.count(), 1)
        self.assertEqual(self.battle1.turnNumber, 1)

    def test_choose_move_good(self):
        self.assertEqual(self.battle1.turnNumber, 1)
        self.assertEqual(self.player1.move_set.count(), 1)
        success = chooseMove(self.player1, 'R')
        self.assertTrue(success)
        self.assertEqual(self.player1.move_set.count(), 2)
        
        move = self.player1.move_set.first()
        self.assertEqual(move.player, self.player1)
        self.assertEqual(move.moveNo, 1)
        self.assertEqual(move.moveUsed, 'R')

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

        self.assertEqual(self.player1.hp, 70)
        self.assertEqual(self.player2.hp, 100)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 0)
        self.assertEqual(self.player2.user.profile.wins, 0)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 2)

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

        success = calculateTurn(self.battle1)
        self.assertTrue(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.assertEqual(self.battle1.status, Battle.FINISHED)
        self.assertEqual(self.battle1.winner, self.player2)
        self.assertEqual(self.player1.currentMove, self.move1)
        self.assertEqual(self.player2.currentMove, self.move2)

        self.assertEqual(self.player1.hp, -10)
        self.assertEqual(self.player2.hp, 100)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 1)
        self.assertEqual(self.player2.user.profile.wins, 1)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 1)
    
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

        success = calculateTurn(self.battle1)
        self.assertTrue(success)

        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.assertEqual(self.battle1.status, Battle.FINISHED)
        self.assertEqual(self.battle1.winner, self.player2)
        self.assertEqual(self.player1.currentMove, self.move1)
        self.assertEqual(self.player2.currentMove, self.move2)

        self.assertEqual(self.player1.hp, -10)
        self.assertEqual(self.player2.hp, 100)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 1)
        self.assertEqual(self.player2.user.profile.wins, 1)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 1)

    def calculate_turn_sanity(self):
        self.assertEqual(self.player1.hp, 100)
        self.assertEqual(self.player2.hp, 100)
        self.assertEqual(self.player1.user.profile.wins, 0)
        self.assertEqual(self.player1.user.profile.losses, 0)
        self.assertEqual(self.player2.user.profile.wins, 0)
        self.assertEqual(self.player2.user.profile.losses, 0)
        self.assertEqual(self.battle1.turnNumber, 1)

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

    def test_ajax_get_battle_status_view_good(self):
        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)

        playerId = self.player1.pk
        response = self.client.get(
            "{url}?playerId={id}".format(url=reverse('getBattleDetails'),
                                         id=playerId))
        self.assertEqual(response.status_code, 200)
        
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

    def test_ajax_create_player_view_good(self):
        players = Player.objects.count()

        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)

        response = self.client.post(reverse('createPlayer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.content), players + 1)
        self.assertEqual(Player.objects.count(), players + 1)

    def test_ajax_start_battle_view_bad(self):
        # Not logged in
        response = self.client.post(reverse('startBattle'))
        self.assertEqual(response.status_code, 403)
        
        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)
        
        # Get
        response = self.client.get(reverse('startBattle'), {})
        self.assertEqual(response.status_code, 400)
        # No playerId given
        response = self.client.post(reverse('startBattle'))
        self.assertEqual(response.status_code, 400)
        # playerID doesn't exist
        playerId = 4
        self.assertFalse(Player.objects.filter(pk=playerId).exists())
        response = self.client.post(
            "{url}?playerId={id}".format(url=reverse('startBattle'),
                                         id=playerId))
        self.assertEqual(response.status_code, 404)
        # Not logged in as user of playerId
        playerId = self.player2.pk
        response = self.client.post(
            "{url}?playerId={id}".format(url=reverse('startBattle'),
                                         id=playerId))
        self.assertEqual(response.status_code, 403)
        # Player is already in a battle
        playerId = self.player1.pk
        response = self.client.post(
            "{url}?playerId={id}".format(url=reverse('startBattle'),
                                         id=playerId))
        self.assertEqual(response.status_code, 400)

    def test_ajax_start_battle_view_good(self):
        # Will only respond with "failure" in cases where multiple players are trying
        # to create battles at once
        # So we only test success case for simplicity
        self.assertFalse(self.player3.isInBattle())
        battles = Battle.objects.count()

        loggedIn = self.client.login(username='staff', password='staffPass')
        self.assertTrue(loggedIn)

        playerId = self.player3.pk
        response = self.client.post(
            "{url}?playerId={id}".format(url=reverse('startBattle'),
                                         id=playerId))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")

        self.player3 = Player.objects.get(user=self.user3)

        self.assertTrue(self.player3.isInBattle())
        self.assertEqual(Battle.objects.count(), battles + 1)
        battle = self.player3.getBattle()
        onePlayer = (((battle.player1 is None) and (not battle.player2 is None)) or
                    ((not battle.player1 is None) and (battle.player2 is None)))
        self.assertTrue(onePlayer)

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
        response = self.client.post(
            "{url}?moveChoice={move}".format(url=reverse('chooseMove'),
                                         move='R'))
        # No moveChoice given
        playerId = self.player3.pk
        response = self.client.post(
            "{url}?playerId={id}".format(url=reverse('chooseMove'),
                                         id=playerId))
        self.assertEqual(response.status_code, 400)
        # moveChoice is invalid
        response = self.client.post(
            "{url}?playerId={id}&moveChoice={move}".format(
                                         url=reverse('chooseMove'),
                                         id=playerId,
                                         move='lol'))
        self.assertEqual(response.status_code, 400)
        # playerID doesn't exist
        playerId = 4
        self.assertFalse(Player.objects.filter(pk=playerId).exists())
        response = self.client.post(
            "{url}?playerId={id}&moveChoice={move}".format(
                                         url=reverse('chooseMove'),
                                         id=playerId,
                                         move='R'))
        self.assertEqual(response.status_code, 404)
        # Not logged in as user of playerId
        playerId = self.player2.pk
        response = self.client.post(
            "{url}?playerId={id}&moveChoice={move}".format(
                                         url=reverse('chooseMove'),
                                         id=playerId,
                                         move='R'))
        self.assertEqual(response.status_code, 403)
        # Player is not in a battle
        playerId = self.player3.pk
        response = self.client.post(
            "{url}?playerId={id}&moveChoice={move}".format(
                                         url=reverse('chooseMove'),
                                         id=playerId,
                                         move='R'))
        self.assertEqual(response.status_code, 400)

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
        response = self.client.post(
            "{url}?playerId={id}&moveChoice={move}".format(
                                         url=reverse('chooseMove'),
                                         id=playerId,
                                         move='R'))
        self.assertEqual(response.status_code, 200)

        self.player1 = Player.objects.get(user=self.user1)

        move = self.player1.currentMove
        self.assertNotEqual(move, lastMove)
        self.assertEqual(Move.objects.count(), moves + 1)
        self.assertEqual(move.player, self.player1)
        self.assertEqual(move.moveUsed, 'R')
        self.assertEqual(move.moveNo, turnNumber)
