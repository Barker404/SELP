from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from battles.models import Move, Player, Battle

class BattlesModelsTestCase(TestCase):
    fixtures = ['auth_user_testdata', 'battles_player_testdata']

    def setUp(self):
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='lewis')
        self.user3 = User.objects.get(username='staff')
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)

    def test_player_save(self):
        print (self.player1)
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

    def test_add_move(self):
        battle = Battle.objects.create(player1=self.player1)
        
        self.assertEqual(Move.objects.count(), 0)
        move = self.player1.addMove(Move.ROCK)

        self.assertEqual(Move.objects.count(), 1)
        self.assertEqual(Move.objects.first(), move)
        self.assertEqual(move.moveUsed, Move.ROCK)
        self.assertEqual(move.player, self.player1)
        self.assertEqual(move.moveNo, 1)
        self.assertEqual(self.player1.currentMove, move)
        self.assertEqual(battle.lastMoveTime, move.time)
        
