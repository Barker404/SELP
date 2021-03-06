from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('home.urls')),
    url(r'^mechs/', include('mechs.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^battle/', include('battles.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
