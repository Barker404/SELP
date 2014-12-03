from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}),
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^account/$', views.accountView, name='account'),
)