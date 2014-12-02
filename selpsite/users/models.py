from django.db import models

class UserProfile(models.Model):
    def __unicode__(self):
        return self.user.username
    # Link UserProfile to User
    user = models.OneToOneField(User)

    # Additional attributes go here
