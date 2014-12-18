from django.test import TestCase

from django.contrib.auth.models import User
from users.models import UserProfile

class UserModelsTestCase(TestCase):
    fixtures = ['auth_user_testdata', 'users_testdata']

    # def setUp(self):
    #     user1 = User.objects.create_user('user1', '', 'user1Pass')
    #     UserProfile.objects.get_or_create(description='user1\'s profile', user=user1)

    # Tests method to calculate the player's score
    def testCalculateScore(self):
        profile = User.objects.get(username='lewis').profile
        self.assertEquals(profile.calculateScore(), 0)

        profile.wins = 5
        self.assertEquals(profile.calculateScore(), 5)
        
        profile.wins = 0
        profile.losses = 5
        self.assertEquals(profile.calculateScore(), 0)

        profile.wins = 10000
        profile.losses = 1
        self.assertEquals(profile.calculateScore(), 10000.0/1.0)

        profile.wins = 10
        profile.losses = 100
        self.assertEquals(profile.calculateScore(), 10.0/100.0)

        profile.wins = 3
        profile.losses = 5
        self.assertEquals(profile.calculateScore(), 3.0/5.0)


    # Tests method to add a win to a player profile
    def testAddWin(self):
        profile = User.objects.get(username='lewis').profile
        self.assertEquals(profile.score, 0)
        self.assertEquals(profile.wins, 0)
        self.assertEquals(profile.losses, 0)

        profile.addWin()
        self.assertEquals(profile.score, 1)
        self.assertEquals(profile.wins, 1)
        self.assertEquals(profile.losses, 0)

        profile.addWin()
        self.assertEquals(profile.score, 2)
        self.assertEquals(profile.wins, 2)
        self.assertEquals(profile.losses, 0)

    # Tests method to add a loss to a player profile
    def testAddLoss(self):
        profile = User.objects.get(username='lewis').profile
        self.assertEquals(profile.score, 0)
        self.assertEquals(profile.wins, 0)
        self.assertEquals(profile.losses, 0)

        profile.addLoss()
        self.assertEquals(profile.score, 0)
        self.assertEquals(profile.wins, 0)
        self.assertEquals(profile.losses, 1)

        profile.addLoss()
        self.assertEquals(profile.score, 0)
        self.assertEquals(profile.wins, 0)
        self.assertEquals(profile.losses, 2)

    # Tests score field of a player's profile
    def testScore(self):
        profile = User.objects.get(username='lewis').profile
        self.assertEquals(profile.score, 0)

        profile.addWin()
        self.assertEquals(profile.score, 1)
        profile.addWin()
        self.assertEquals(profile.score, 2)
        profile.addLoss()
        self.assertEquals(profile.score, 2)
        profile.addLoss()
        self.assertEquals(profile.score, 1)
        profile.addLoss()
        self.assertEquals(profile.score, 2.0/3.0)


