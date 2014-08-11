from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls.static import static

from oscar.app import shop
from oscar.views import handler500, handler404, handler403  # noqa

from apps.sitemaps import base_sitemaps
from apps.api import *

admin.autodiscover()


urlpatterns = [
    # Include admin as convenience. It's unsupported and you should
    # use the dashboard
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('apps.api.urls')),
    url(r'^editor/', include('apps.editor.urls')),
<<<<<<< HEAD
    url(r'^library/', include('apps.library.urls')),
=======
    url(r'^mepin/', include('apps.mepin.urls')),
>>>>>>> b97bdd0424269147c89618bff23af953f1263b8b
    # i18n URLS need to live outside of i18n_patterns scope of the shop
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # include a basic sitemap
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {
        'sitemaps': base_sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap', {'sitemaps': base_sitemaps}),
    #
    url(r'^ajax/$', 'apps.ajax.home.loadItems'),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]

# Prefix Oscar URLs with language codes
urlpatterns += i18n_patterns('',
    # Custom functionality to allow dashboard users to be created
    url(r'gateway/', include('apps.gateway.urls')),

    # Oscar's normal URLs
    url(r'', include(shop.urls)),
)

if settings.DEBUG:
    import debug_toolbar

    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        url(r'^403$', handler403),
        url(r'^404$', handler404),
        url(r'^500$', handler500),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

