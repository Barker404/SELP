from django.conf.urls import patterns, url

from mechs import views

urlpatterns = patterns('',
  url(r'^$', views.index.as_view(), name='index'),
  url(r'^detail/(?P<pk>\d+)/$', views.detail.as_view(), name='detail'),
)