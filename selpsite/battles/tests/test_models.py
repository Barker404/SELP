from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from battles.models import Move, Player, Battle

class BattlesViewsTestCase(TestCase):
    fixtures = ['auth_user_testdata']

    def test_player_save(self):
        print (User.objects.all())
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='lewis')
        user3 = User.objects.get(username='staff')
        player1 = Player.objects.create(user=user1)
        player2 = Player.objects.create(user=user2)
        player3 = Player.objects.create(user=user3)
        self.assertIsNone(player1.opponent)
        self.assertIsNone(player2.opponent)
        self.assertIsNone(player3.opponent)
        player1.opponent = player2
        player1.save()
        self.assertEqual(player2.opponent, player1)
        player1.opponent = None
        player1.save()
        player3.opponent = player2
        player3.save()
        self.assertEqual(player2.opponent, player3)

    def test_add_move(self):
        user1 = User.objects.get(username='user1')
        player1 = Player.objects.create(user=user1)
        battle = Battle.objects.create(player1=player1)
        
        self.assertEqual(Move.objects.count(), 0)
        move = player1.addMove(Move.ROCK)

        self.assertEqual(Move.objects.count(), 1)
        self.assertEqual(Move.objects.first(), move)
        self.assertEqual(move.moveUsed, Move.ROCK)
        self.assertEqual(move.player, player1)
        self.assertEqual(move.moveNo, 1)
        self.assertEqual(player1.currentMove, move)
        self.assertEqual(battle.lastMoveTime, move.time)


