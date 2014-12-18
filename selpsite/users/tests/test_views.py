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

    # Tests GETing the register form
    def test_register_get(self):
        # Check that the register view shows correctly initially
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('userForm' in response.context)
        self.assertTrue('profileForm' in response.context)

    # Tests POSTing the register form with good input
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

    # Tests POSTing the register form with various bad inputs
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

    # Tests the response from the welcome view
    def test_welcome_view(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)

    # Tests the response from the login view
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    # Tests the response from the logout view
    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    # Tests the response from the account view when the user is logged in
    def test_account_auth(self):
        # Check account when logged in
        loggedIn = self.client.login(username='user1', password='user1Pass')
        self.assertTrue(loggedIn)
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    # Tests the response from the account view when the user is not 
    # logged in
    def test_account_unauth(self):
        # Check that account reiderects unauthorised clients
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, '/users/login/?next=/users/account/', 
            status_code=302, target_status_code=200)

    # Tests the user detail view and the context returned by it for various 
    # users
    def test_user_detail_view(self):
        lewis = User.objects.get(username='lewis')
        user1 = User.objects.get(username='user1')
        response = self.client.get(reverse('userDetail', args=('lewis',)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('detailUser' in response.context)
        self.assertEqual(response.context['detailUser'], lewis)

        response = self.client.get(reverse('userDetail', args=('user1',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('detailUser' in response.context)
        self.assertEqual(response.context['detailUser'], user1)

        response = self.client.get(reverse('userDetail', args=('not_a_user',)))
        self.assertEqual(response.status_code, 404)

    # Tests the tankings view and the context returned by it
    def test_rankings_view(self):
        lewis = User.objects.get(username='lewis')
        user1 = User.objects.get(username='user1')
        response = self.client.get(reverse('rankings'))
        self.assertTrue('ranked_users' in response.context)
        self.assertTrue(lewis in response.context['ranked_users'])
        self.assertTrue(user1 in response.context['ranked_users'])
        self.assertEqual(response.status_code, 200)

    # Tests the rankedUser function which returns the list of users in 
    # score order
    def test_get_rankings(self):
        lewis = User.objects.get(username='lewis')
        user1 = User.objects.get(username='user1')
        lewis.profile.addWin()
        lewis.profile.save()
        self.assertEqual(lewis.profile.score, 1)
        self.assertEqual(user1.profile.score, 0)

        rankings = rankedUsers()
        self.assertEqual(rankings[0], lewis)

        user1.profile.addWin()
        user1.profile.addWin()
        user1.profile.save()
        self.assertEqual(lewis.profile.score, 1)
        self.assertEqual(user1.profile.score, 2)
        newRankings = rankedUsers()
        self.assertEqual(newRankings[0], user1)
        self.assertEqual(newRankings[1], lewis)

    # Tests the user detail view for users whose names contain special characters
    def test_user_details_view_special_characters(self):
        userCount = User.objects.count()
        profileCount = UserProfile.objects.count()

        username = "-name.with@special+chars_"
        password = "@pass.with+special!chars?"
        user = User.objects.create(username=username, password=password)
        profile = UserProfile.objects.create(user=user)

        self.assertEqual(User.objects.count(), userCount + 1)
        self.assertEqual(UserProfile.objects.count(), profileCount + 1)

        response = self.client.get(reverse('userDetail', args=(username,)))
        self.assertEqual(response.status_code, 200)

