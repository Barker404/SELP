from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

def registerView(request):
    if request.method == 'POST':
        # Post the data
        return
    else:
        # Show registration forms
        # Standard django user form, plus model form for UserProfile
        return

def accountView(request):
    # Redirect to login page if user is not logged in
    if not request.user.is_authenticated():
        return redirect('/users/login/?next=%s' % request.path)
    else:
        return render(request, 'users/account.html')
