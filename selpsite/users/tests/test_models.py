from django.test import TestCase

from django.contrib.auth.models import User
from users.models import UserProfile

class UserModelsTestCase(TestCase):
    fixtures = ['auth_user_testdata', 'users_testdata']

    # def setUp(self):
    #     user1 = User.objects.create_user('user1', '', 'user1Pass')
    #     UserProfile.objects.get_or_create(description='user1\'s profile', user=user1)

    def testScore(self):
        testUser = User.objects.create_user(username='test1', password='test1Pass')
        profile = UserProfile.objects.create(user=testUser, description='') 
        self.assertEquals(profile.calculateScore(), 0)

        testUser = User.objects.create_user(username='test2', password='test2Pass')
        profile = UserProfile.objects.create(user=testUser, description='', wins=5) 
        self.assertEquals(profile.calculateScore(), 5)
        
        testUser = User.objects.create_user(username='test3', password='test3Pass')
        profile = UserProfile.objects.create(user=testUser, description='', losses=5) 
        self.assertEquals(profile.calculateScore(), 0)

        testUser = User.objects.create_user(username='test4', password='test4Pass')
        profile = UserProfile.objects.create(user=testUser, description='', wins=10000, losses=1) 
        self.assertEquals(profile.calculateScore(), 10000)

        testUser = User.objects.create_user(username='test5', password='test5Pass')
        profile = UserProfile.objects.create(user=testUser, description='', wins=10, losses=100) 
        self.assertEquals(profile.calculateScore(), 10/100)