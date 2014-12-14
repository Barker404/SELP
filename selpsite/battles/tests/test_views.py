from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from battles.models import Move, Player, Battle
from battles.views import joinBattle

class BattlesViewsTestCase(TestCase):
    fixtures = ['auth_user_testdata', 'battles_player_testdata']

    def setUp(self):
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='lewis')
        self.user3 = User.objects.get(username='staff')
        self.player1 = Player.objects.get(user=self.user1)
        self.player2 = Player.objects.get(user=self.user2)
        self.player3 = Player.objects.get(user=self.user3)

    def test_start_battle_view(self):
        response = self.client.get(reverse('startBattle'))
        self.assertEqual(response.status_code, 200)

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
