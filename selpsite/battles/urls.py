from django.conf.urls import patterns, url

from battles import views

urlpatterns = patterns('',
    url(r'^$', views.startBattleView, name='startBattle'),
)
