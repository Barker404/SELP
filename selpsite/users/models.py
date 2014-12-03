from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    def __unicode__(self):
        return self.user.username
    # Link UserProfile to User
    user = models.OneToOneField(User)

    # Additional attributes go here
