from django.test import TestCase
from django.core.urlresolvers import reverse

class HomeViewsTestCase(TestCase):

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)