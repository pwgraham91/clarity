from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'speed_date.views.index', name='index'),
    url(r'^caller/$', 'speed_date.views.caller', name='caller'),
    url(r'^callee/$', 'speed_date.views.callee', name='callee'),
)
