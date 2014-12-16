from django.conf.urls import patterns, url

from battles import views

urlpatterns = patterns('',
    url(r'getBattleStatus', views.ajaxGetBattleStatusView, name='getBattleStatus'),
    url(r'^$', views.startBattleView, name='startBattle'),
)
