from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

# View for creating account
# - Confirmation screen?

def accountView(request):
    # Redirect to login page if user is not logged in
    if not request.user.is_authenticated():
        return redirect('/users/login/?next=%s' % request.path)
    else:
        return render(request, 'users/account.html', { 'user': request.user })
