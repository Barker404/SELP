from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^register/$', views.registerView, name='register'),
    url(r'^welcome/$', views.welcomeView, name='welcome'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'users/logout.html'}, name='logout'),
    url(r'^account/$', views.accountView, name='account'),
    url(r'^detail/(?P<user_id>\w+)/$', views.userDetailView, name='userDetail'),
    url(r'^rankings/$', views.RankingView.as_view(), name='rankings'),
)
