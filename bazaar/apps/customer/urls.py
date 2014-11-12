from distutils.version import StrictVersion
import django
if StrictVersion(django.get_version()) < StrictVersion('1.4'):
    from django.conf.urls.defaults import *
else:
    from django.conf.urls import patterns, url

from views import ShibbolethView, ShibbolethLogoutView, AccountAuthView

urlpatterns = patterns('',
    url(r'^login/$', AccountAuthView.as_view(), name='login'),
    url(r'^logout/$', ShibbolethLogoutView.as_view(), name='logout'),
    url(r'^$', ShibbolethView.as_view(), name='info'),
)