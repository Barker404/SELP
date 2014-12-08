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
    
    def score(self):
        return self.wins/self.losses