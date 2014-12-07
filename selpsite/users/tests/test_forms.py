from django.test import TestCase

class UsersFormsTestCase(TestCase):
    fixtures = ['auth_user_testdata', 'users_testdata']
b
    # def setUp(self):
    #     user1 = User.objects.create_user('user1', '', 'user1Pass')
    #     UserProfile.objects.get_or_create(description='user1\'s profile', user=user1)

