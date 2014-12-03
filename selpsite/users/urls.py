from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'users/logout.html'}, name='logout'),
    url(r'^account/$', views.accountView, name='account'),
)