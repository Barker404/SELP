from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from battles.models import Move, Player, Battle
from battles.views import joinBattle, chooseMove, calculateTurn

class BattlesViewsTestCase_Views(TestCase):

    def test_start_battle_view(self):
        response = self.client.get(reverse('startBattle'))
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
                'battles_player_testdata', 
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
