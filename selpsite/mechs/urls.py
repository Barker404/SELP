from django.conf.urls import patterns, url
from mechs import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  # ex: /mechs/5/
  url(r'^detail/(?P<mech_id>\d+)/$', views.detail, name='detail'),
)