import os, sys

# Path helper
PROJECT_DIR = os.path.dirname(__file__)
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

USE_TZ = True

DEBUG = True
TEMPLATE_DEBUG = True
SQL_DEBUG = True

ALLOWED_HOSTS = ['latest.oscarcommerce.com',
                 'sandbox.oscar.tangentlabs.co.uk',
                 'master.oscarcommerce.com']

ADMINS = (
    ('Admin Adminton', 'admin@admin.com'),
)

EMAIL_SUBJECT_PREFIX = '[Basaar] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MANAGERS = ADMINS

# Use a Sqlite database by default
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': location('db.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Helsinki'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fi'

# Includes all languages that have >50% coverage in Transifex
# Taken from Django's default setting for LANGUAGES
gettext_noop = lambda s: s
LANGUAGES = (
    ('en-gb', gettext_noop('British English')),
    ('fi', gettext_noop('Finnish')),
    ('sv', gettext_noop('Swedish')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = location("public/media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/admin/'

STATIC_URL = '/static/'
STATIC_ROOT = location('public/static')
STATICFILES_DIRS = (
    location('static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'zxb+gy#^d!%ty#4+hf_u=jy6)tty962qnhqwcl1c^9i^!j7nx='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # needed by django-treebeard for admin (and potentially other libs)
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    # Oscar specific
    'apps.search.context_processors.search_form',
    'oscar.apps.promotions.context_processors.promotions',
    'oscar.apps.checkout.context_processors.checkout',
    'oscar.core.context_processors.metadata',
    'oscar.apps.customer.notifications.context_processors.notifications',
    # Shibboleth
    'apps.customer.context_processors.login_link',
    'apps.customer.context_processors.logout_link',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Shibboleth RemoteUserMiddleware
    'apps.customer.middleware.ShibbolethRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Allow languages to be selected
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    # Ensure a valid basket is added to the request instance for every request
    'oscar.apps.basket.middleware.BasketMiddleware',
    # Enable the ProfileMiddleware, then add ?cprofile to any
    # URL path to print out profile details
    #'oscar.profiling.middleware.ProfileMiddleware',
    'cookie_message.middleware.CookieMessageMiddleware',
)

ROOT_URLCONF = 'urls'

# Add another path to Oscar's templates.  This allows templates to be
# customised easily.
from oscar import OSCAR_MAIN_TEMPLATE_DIR
TEMPLATE_DIRS = (
    location('templates'),
    OSCAR_MAIN_TEMPLATE_DIR,
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
        'simple': {
            'format': '[%(asctime)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'checkout_file': {
            'level': 'INFO',
            'class': 'oscar.core.logging.handlers.EnvFileHandler',
            'filename': 'checkout.log',
            'formatter': 'verbose'
        },
        'gateway_file': {
            'level': 'INFO',
            'class': 'oscar.core.logging.handlers.EnvFileHandler',
            'filename': 'gateway.log',
            'formatter': 'simple'
        },
        'error_file': {
            'level': 'INFO',
            'class': 'oscar.core.logging.handlers.EnvFileHandler',
            'filename': 'errors.log',
            'formatter': 'verbose'
        },
        'sorl_file': {
            'level': 'INFO',
            'class': 'oscar.core.logging.handlers.EnvFileHandler',
            'filename': 'sorl.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        # Django loggers
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        # Oscar core loggers
        'oscar.checkout': {
            'handlers': ['console', 'checkout_file'],
            'propagate': False,
            'level': 'INFO',
        },
        'oscar.catalogue.import': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
        'oscar.alerts': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'INFO',
        },
        # Sandbox logging
        'gateway': {
            'handlers': ['gateway_file'],
            'propagate': True,
            'level': 'INFO',
        },
        # Third party
        'south': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'sorl.thumbnail': {
            'handlers': ['sorl_file'],
            'propagate': True,
            'level': 'INFO',
        },
        # Suppress output of this debug toolbar panel
        'template_timings_panel': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

from oscar import get_core_apps
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_extensions',
    #Shibboleth_test
    'apps.test_shibboleth',
    # Debug toolbar + extensions
    'debug_toolbar',
    'template_timings_panel',
    'south',
    'compressor',       # Oscar's templates use compressor
    'apps.gateway',     # For allowing dashboard access
    'apps.api',
    'apps.editor',
    'apps.library',
    'rest_framework',
    'provider',
    'provider.oauth2',
    'apps.user',
    'cookie_message',
    'rest_framework_swagger',
    'haystack',
    'json_field',       #https://github.com/derek-schaefer/django-json-field
] + get_core_apps(['apps.catalogue', 'apps.search', 'apps.order', 'apps.customer.*', 'apps.checkout'])

# Bazaar User model
AUTH_USER_MODEL = "user.User"

AUTHENTICATION_BACKENDS = (
    #'oscar.apps.customer.auth_backends.Emailbackend',
    #'django.contrib.auth.backends.ModelBackend',
    'apps.customer.auth_backends.ShibbolethRemoteUserBackend',
)

#Shibboleth
SHIBBOLETH_LOGIN_URL = 'https://test.pilvivayla.fi/Shibboleth.sso/Login'

SHIBBOLETH_ATTRIBUTE_MAP = {
   "HTTP_SHIB_USER": (True, "username"),
   "HTTP_SHIB_GIVEN_NAME": (True, "first_name"),
   "HTTP_SHIP_SN": (True, "last_name"),
   "HTTP_SHIB_MAIL": (False, "email"),
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',
    'rest_framework.permissions.DjangoModelPermissions',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.OAuth2Authentication',),
    'PAGINATE_BY': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.UnicodeJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

}

LOGIN_REDIRECT_URL = '/'
APPEND_SLASH = True

# Haystack settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/',
        'INCLUDE_SPELLING': True,
    },
}


# =============
# Debug Toolbar
# =============

# Implicit setup can often lead to problems with circular imports, so we
# explicitly wire up the toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
INTERNAL_IPS = ['127.0.0.1', '::1']

# ==============
# Oscar settings
# ==============

from oscar.defaults import *

# Meta
# ====

#OSCAR_SHOP_TAGLINE = 'Bazaar'
OSCAR_SHOP_NAME = 'Bazaar'

OSCAR_RECENTLY_VIEWED_PRODUCTS = 20
OSCAR_ALLOW_ANON_CHECKOUT = False
OSCAR_ALLOW_ANON_REVIEWS = False
OSCAR_MODERATE_REVIEWS = False
OSCAR_EAGER_ALERTS = False
OSCAR_SEND_REGISTRATION_EMAIL = False
OSCAR_CURRENCY_LOCALE = 'fi_FI'
OSCAR_DEFAULT_CURRENCY = 'EUR'
OSCAR_CURRENCY_LOCALE = 'fi_FI'



# This is added to each template context by the core context processor.  It is
# useful for test/stage/qa sites where you want to show the version of the site
# in the page title.
DISPLAY_VERSION = False


# Order processing
# ================

# Sample order/line status settings. This is quite simplistic. It's like you'll
# want to override the set_status method on the order object to do more
# sophisticated things.
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'

# This dict defines the new order statuses than an order can move to
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Complete', 'Cancelled',),
    'Cancelled': (),
    'Complete': (),
}

# This dict defines the line statuses that will be set when an order's status
# is changed
OSCAR_ORDER_STATUS_CASCADE = {
    'Being processed': 'Being processed',
    'Cancelled': 'Cancelled',
    'Complete': 'Shipped',
}


# LESS/CSS/statics
# ================

# We default to using CSS files, rather than the LESS files that generate them.
# If you want to develop Oscar's CSS, then set USE_LESS=True and
# COMPRESS_ENABLED=False in your settings_local module and ensure you have
# 'lessc' installed.  You can do this by running:
#
#    pip install -r requirements_less.txt
#
# which will install node.js and less in your virtualenv.

USE_LESS = False

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': 'STATIC_URL',
    'use_less': USE_LESS,
}

# We do this to work around an issue in compressor where the LESS files are
# compiled but compression isn't enabled.  When this happens, the relative URL
# is wrong between the generated CSS file and other assets:
# https://github.com/jezdez/django_compressor/issues/226
COMPRESS_OUTPUT_DIR = 'oscar'

# Logging
# =======

LOG_ROOT = location('logs')
# Ensure log root exists
if not os.path.exists(LOG_ROOT):
    os.mkdir(LOG_ROOT)

# Sorl
# ====

THUMBNAIL_DEBUG = True
THUMBNAIL_KEY_PREFIX = 'bazaar-'

# Use a custom KV store to handle integrity error
THUMBNAIL_KVSTORE = 'oscar.sorl_kvstore.ConcurrentKVStore'

# Django 1.6 has switched to JSON serializing for security reasons, but it does not
# serialize Models. We should resolve this by extending the
# django/core/serializers/json.Serializer to have the `dumps` function. Also
# in tests/config.py
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Try and import local settings which can be used to override any of the above.
try:
    from settings_local import *
except ImportError:
    pass
