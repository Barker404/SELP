from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from battles.models import Move, Player, Battle

class BattlesModelsTestCase(TestCase):
    fixtures = ['auth_user_testdata',
                'battles_player_testdata']

    def setUp(self):
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='lewis')
        self.user3 = User.objects.get(username='staff')
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)

    # Tests saving a player will correctly set the opponent's opponent 
    # to the current player
    def test_player_save(self):
        self.assertIsNone(self.player1.opponent)
        self.assertIsNone(self.player2.opponent)
        self.assertIsNone(self.player3.opponent)
        
        self.player1.opponent = self.player2
        self.player1.save()
        self.assertEqual(self.player2.opponent, self.player1)

        self.player1.opponent = None
        self.player1.save()
        self.player3.opponent = self.player2
        self.player3.save()
        self.assertEqual(self.player2.opponent, self.player3)

    # Tests the method for adding a move to a player in the good case
    def test_add_move(self):
        battle = Battle.objects.create(player1=self.player1)
        
        self.assertEqual(Move.objects.count(), 0)
        move = self.player1.addMove(Move.SHORT_RANGE)

        self.assertEqual(Move.objects.count(), 1)
        self.assertEqual(Move.objects.first(), move)
        self.assertEqual(move.moveUsed, Move.SHORT_RANGE)
        self.assertEqual(move.player, self.player1)
        self.assertEqual(move.moveNo, 1)
        self.assertEqual(self.player1.currentMove, move)
        self.assertEqual(battle.lastMoveTime, move.time)

    # Tests the method for adding a move to a player in the case where
    # the player is not part of a battle
    def test_add_move_no_battle(self):
        # Player is in no battle
        self.assertEqual(Move.objects.count(), 0)
        move = self.player1.addMove(Move.SHORT_RANGE)

        self.assertIsNone(move)
        self.assertEqual(Move.objects.count(), 0)
        self.assertEqual(self.player1.currentMove, None)

    # Tests Battle.tryAddPlayer where there are no other players in the 
    # battle
    def test_try_add_player_only(self):
        battle = Battle.objects.create()
        success = battle.tryAddPlayer(self.player1)
        self.assertTrue(success)

        self.assertEqual(battle.player1, self.player1)

    # Tests Battle.tryAddPlayer where there is already a player 2 in the
    # battle
    def test_try_add_player_one(self):
        self.assertIsNone(self.player1.opponent)
        self.assertIsNone(self.player2.opponent)

        battle = Battle.objects.create(player2=self.player2)
        success = battle.tryAddPlayer(self.player1)
        self.assertTrue(success)

        self.assertEqual(battle.player1, self.player1)
        self.assertEqual(self.player1.opponent, self.player2)
        self.assertEqual(self.player2.opponent, self.player1)

    # Tests Battle.tryAddPlayer where there is already a player 1 in the
    # battle
    def test_try_add_player_two(self):
        self.assertIsNone(self.player1.opponent)
        self.assertIsNone(self.player2.opponent)

        battle = Battle.objects.create(player1=self.player1)
        success = battle.tryAddPlayer(self.player2)
        self.assertTrue(success)

        self.assertEqual(battle.player2, self.player2)
        self.assertEqual(self.player2.opponent, self.player1)
        self.assertEqual(self.player1.opponent, self.player2)

class BattlesModelsTestCase_ExistingBattle(TestCase):
    fixtures = ['auth_user_testdata',
                'battles_player_opponents_testdata', 
                'battles_battle_testdata']

    def setUp(self):
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='lewis')
        self.user3 = User.objects.get(username='staff')
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)
        self.battle1 = Battle.objects.first()

    # Tests Battle.tryAddPlayer where there is no space for another 
    # player in the battle
    def test_try_add_player_no_space(self):
        success = self.battle1.tryAddPlayer(self.player3)
        self.assertFalse(success)

    # Test Player.getPlayerNumber()
    def test_get_player_number(self):
        p1 = self.player1.getPlayerNumber()
        self.assertEqual(p1, 1)
        p2 = self.player2.getPlayerNumber()
        self.assertEqual(p2, 2)
        p3 = self.player3.getPlayerNumber()
        self.assertEqual(p3, 0)

    # Test Player.getBattle()
    def test_get_battle(self):
        p1 = self.player1.getBattle()
        self.assertEqual(p1, self.battle1)
        p2 = self.player2.getBattle()
        self.assertEqual(p2, self.battle1)
        p3 = self.player3.getBattle()
        self.assertIsNone(p3)

    # Test Player.isInBattle()
    def test_is_in_battle(self):
        p1 = self.player1.isInBattle()
        self.assertTrue(p1)
        p2 = self.player2.isInBattle()
        self.assertTrue(p2)
        p3 = self.player3.isInBattle()
        self.assertFalse(p3)
