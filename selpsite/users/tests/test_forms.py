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
