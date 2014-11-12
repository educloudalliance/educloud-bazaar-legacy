from django.conf.urls import patterns, url
from django.contrib import admin

from apps.panel import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^products/$', views.products, name='products'),
    url(r'^products/new/$', views.new, name='new'),
    url(r'^products/edit/(?P<productUpc>\w+)/$', views.edit, name='edit'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^help/$', views.help, name='help'),
    #url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
)