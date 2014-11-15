from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'speed_date.views.index', name='index'),
    url(r'^caller/$', 'speed_date.views.caller', name='caller'),
    url(r'^callee/$', 'speed_date.views.callee', name='callee'),
    url(r'^home/$', 'speed_date.views.home', name='home'),
    url(r'^loc/$', 'speed_date.views.loc', name='loc'),
    url('', include('social.apps.django_app.urls', namespace='social'))
)
