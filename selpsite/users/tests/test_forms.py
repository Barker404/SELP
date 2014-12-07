from django.test import TestCase

from django.contrib.auth.models import User
from users.models import UserProfile

class UsersFormsTestCase(TestCase):
    fixtures = ['auth_user_testdata', 'users_testdata']

    # def setUp(self):
    #     user1 = User.objects.create_user('user1', '', 'user1Pass')
    #     UserProfile.objects.get_or_create(description='user1\'s profile', user=user1)

    def test_good_register(self):
        newUsername ='user2'
        newPassword = 'user2Pass'
        newDescription = 'this is a test'

        # Check we can create a user properly
        response = self.client.post('/users/register/', {
            'userForm-username' : newUsername, 
            'userForm-password1' : newPassword, 
            'userForm-password2' : newPassword, 
            'profileForm-description' : newDescription})
        self.assertRedirects(response, '/users/welcome/', 
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
        response = self.client.post('/users/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), noUsers)
        self.assertEqual(UserProfile.objects.count(), noProfiles)

        # Existing username
        self.assertTrue(User.objects.filter(username='user1').exists())
        response = self.client.post('/users/register/', {
            'userForm-username' : 'user1', 
            'userForm-password1' : 'password', 
            'userForm-password2' : 'password', 
            'profileForm-description' : 'hi'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), noUsers)
        self.assertEqual(UserProfile.objects.count(), noProfiles)

        # Different passwords
        self.assertTrue(User.objects.filter(username='user1').exists())
        response = self.client.post('/users/register/', {
            'userForm-username' : 'newUser', 
            'userForm-password1' : 'passworda', 
            'userForm-password2' : 'passwordb', 
            'profileForm-description' : 'hi'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), noUsers)
        self.assertEqual(UserProfile.objects.count(), noProfiles)
