from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'speed_date.views.index', name='index'),
    url(r'^caller/$', 'speed_date.views.caller', name='caller'),
    url(r'^callee/$', 'speed_date.views.callee', name='callee'),
    url(r'^home/$', 'speed_date.views.home', name='home'),
    url(r'^loc/$', 'speed_date.views.loc', name='loc'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^chat_messages/(?P<dater_username>\w+)/$', 'speed_date.views.chat_messages', name='chat_messages'),
    url(r'^chat_with/(?P<dater_username>\w+)/$', 'speed_date.views.chat_with', name='chat_with'),
    url(r'^gender/(?P<user_gender>\w+)/(?P<user_preference>\w+)/$', 'speed_date.views.gender', name='gender'),
    url(r'^new_message/$', 'speed_date.views.new_message', name='new_message'),
    url(r'^online/$', 'speed_date.views.online', name='online'),
    url(r'^liked/(?P<dater_username>\w+)/$', 'speed_date.views.liked', name='liked'),
    url(r'^flag/(?P<offensive>\w+)/$', 'speed_date.views.flag', name='flag'),
    url(r'^fifty/(?P<friends>\w+)/$', 'speed_date.views.fifty', name='fifty'),
    url(r'^fb_link/(?P<link>\w+)/$', 'speed_date.views.fb_link', name='fb_link'),



)
