from django import forms
from django.forms import ModelForm
from users.models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['description']
        