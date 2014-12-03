from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

# View for creating account
# - Confirmation screen?

def logoutView(request):
    logout(request)
    return HttpResponse("Logged out successfully")

