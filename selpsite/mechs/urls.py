from django.conf.urls import patterns, url

from mechs import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^detail/(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)
