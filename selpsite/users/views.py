from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from users.forms import UserProfileForm

def registerView(request):
    if request.method == 'POST':
        # POST: create forms and populate with request data
        userForm = UserCreationForm(request.POST, prefix="userForm");
        profileForm = UserProfileForm(request.POST, prefix="profileForm");

        if (userForm.is_valid() and profileForm.is_valid()):
            savedUser = userForm.save()
            # Save profile without committing, so we can manually add the user
            savedProfile = profileForm.save(commit=False)
            savedProfile.user = savedUser
            savedProfile.save()
            savedUser.save()
            return redirect(reverse('welcome'))
    else:
        # GET (or other method): create blank forms
        userForm = UserCreationForm(prefix="userForm");
        profileForm = UserProfileForm(prefix="profileForm");
    
    # Render template with forms
    return render(request, 'users/register.html', 
        {'userForm': userForm, 'profileForm' : profileForm})

def accountView(request):
    # Redirect to login page if user is not logged in
    if not request.user.is_authenticated():
        return redirect('/users/login/?next=%s' % request.path)
    else:
        return render(request, 'users/account.html')

def welcomeView(request):
    return render(request, 'users/welcome.html')


class RankingView(generic.ListView):
    model = User
    template_name = 'users/rankings.html'
    context_object_name = 'ranked_users'

    def get_queryset(self):
        """Return the user in order of ranking."""
        return rankedUsers()

def rankedUsers():
    # Can change this if we want to sort by something other than score
    return User.objects.order_by('-profile__score')
    