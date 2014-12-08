from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from users.models import UserProfile

from users.views import rankedUsers

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

    def test_good_register(self):
        newUsername ='user2'
        newPassword = 'user2Pass'
        newDescription = 'this is a test'

        # Check we can create a user properly
        response = self.client.post(reverse('register'), {
            'userForm-username' : newUsername, 
            'userForm-password1' : newPassword, 
            'userForm-password2' : newPassword, 
            'profileForm-description' : newDescription})
        self.assertRedirects(response, reverse('welcome'), 
            status_code=302, target_status_code=200)

        # Check we can then log in
        loggedIn = self.client.login(username=newUsername, password=newPassword)
        self.assertTrue(loggedIn)
        self.assertIn('_auth_user_id', self.client.session)

        # Check that the profile has been made correctly
        user = User.objects.get(username=newUsername)
        self.assertEqual(user.profile.description, newDescription)

    def test_bad_register(self):
        # A lot of these are testing Django's own form, but best to be safe
        # Store number of users and profiles
        noUsers = User.objects.count()
        noProfiles = UserProfile.objects.count()

        # Empty post
        response = self.client.post(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), noUsers)
        self.assertEqual(UserProfile.objects.count(), noProfiles)

        # Existing username
        self.assertTrue(User.objects.filter(username='user1').exists())
        response = self.client.post(reverse('register'), {
            'userForm-username' : 'user1', 
            'userForm-password1' : 'password', 
            'userForm-password2' : 'password', 
            'profileForm-description' : 'hi'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), noUsers)
        self.assertEqual(UserProfile.objects.count(), noProfiles)

        # Different passwords
        self.assertTrue(User.objects.filter(username='user1').exists())
        response = self.client.post(reverse('register'), {
            'userForm-username' : 'newUser', 
            'userForm-password1' : 'passworda', 
            'userForm-password2' : 'passwordb', 
            'profileForm-description' : 'hi'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), noUsers)
        self.assertEqual(UserProfile.objects.count(), noProfiles)

    def test_rankings_view(self):
        lewis = User.objects.get(username='lewis')
        user1 = User.objects.get(username='user1')
        response = self.client.get(reverse('rankings'))
        self.assertTrue('ranked_users' in response.context)
        self.assertTrue(lewis in response.context['ranked_users'])
        self.assertTrue(user1 in response.context['ranked_users'])
        self.assertEqual(response.status_code, 200)

    def test_get_rankings(self):
        lewis = User.objects.get(username='lewis')
        user1 = User.objects.get(username='user1')
        lewis.profile.addWin()
        self.assertEqual(lewis.profile.score, 1)
        self.assertEqual(user1.profile.score, 0)

        rankings = rankedUsers()
        self.assertEqual(rankings[0], lewis)

        user1.profile.addWin()
        user1.profile.addWin()
        self.assertEqual(lewis.profile.score, 1)
        self.assertEqual(user1.profile.score, 2)
        rankings = rankedUsers()
        # print(rankings)
        # self.assertEqual(rankings[0], user1)
        # self.assertEqual(rankings[1], lewis)


