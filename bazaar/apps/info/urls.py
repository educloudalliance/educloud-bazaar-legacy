from django.conf.urls import patterns, url
from django.contrib import admin

from apps.info import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^rekisteriseloste/$', views.rekisteri, name='rekisteri'),
)