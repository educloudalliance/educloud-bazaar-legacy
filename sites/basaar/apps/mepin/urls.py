from django.conf.urls import patterns, url
from django.contrib import admin

from apps.mepin import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^edit/(?P<productUpc>\w+)/$', views.edit, name='edit'),
    #url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
)