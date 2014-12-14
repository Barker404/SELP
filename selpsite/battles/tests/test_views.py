from django.test import TestCase
from django.core.urlresolvers import reverse

class BattlesViewsTestCase(TestCase):

    def test_start_battle_view(self):
        response = self.client.get(reverse('startBattle'))
        self.assertEqual(response.status_code, 200)
        