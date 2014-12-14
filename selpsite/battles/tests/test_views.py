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
