from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from users.models import UserProfile

class UsersViewsTestCase(TestCase):
    fixtures = ['auth_user_testdata', 'users_testdata']

    # def setUp(self):
    #     user1 = User.objects.create_user('user1', '', 'user1Pass')
    #     UserProfile.objects.get_or_create(description='user1\'s profile', user=user1)

    def test_register_get(self):
        # Check that the register view shows correctly initially
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('userForm' in response.context)
        self.assertTrue('profileForm' in response.context)

    def test_account_unauth(self):
        # Check that account reiderects unauthorised clients
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, '/users/login/?next=/users/account/', 
            status_code=302, target_status_code=200)

    def test_account_auth(self):
        # Check account when logged in
        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_welcome_view(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
