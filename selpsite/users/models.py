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
    
    # This defines how users are ranked
    def score(self):
        if (self.losses == 0):
            return self.wins
        else:
            return self.wins/self.losses