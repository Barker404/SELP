from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

# View for creating account
# - Confirmation screen?

# View for logging in
# - success/failure screen?
# - need to figure out sessions/cookies

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse("Logged in successfully as %s." % username)
        else:
            return HttpResponse("Account disabled")
    else:
        return HttpResponse("Login failed")


def logout(request):
    logout(request)
    return HttpResponse("Logged out successfully")