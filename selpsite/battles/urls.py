from django.conf.urls import patterns, url

from battles import views

urlpatterns = patterns('',
    url(r'createPlayer', views.ajaxCreatePlayerView, name='createPlayer'),
    url(r'getBattleDetails', views.ajaxGetBattleDetailsView, name='getBattleDetails'),
    url(r'^$', views.startBattleView, name='startBattle'),
)
