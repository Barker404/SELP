from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    def __unicode__(self):
        return self.user.username
    # Link UserProfile to User
    user = models.OneToOneField(User, related_name="profile")
    # Additional attributes
    description = models.TextField(blank=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    score = models.FloatField(default = 0)

    # This defines how users are ranked
    def calculateScore(self):
        if (self.losses == 0):
            return self.wins
        else:
            return self.wins/self.losses

    def addWin(self):
        self.wins = self.wins + 1
        self.score = self.calculateScore()

    def addLoss(self):
        self.losses = self.losses + 1
        self.score = self.calculateScore()
