# Django settings for ratings project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os.path
import sys

PROJECT_ROOT = os.path.dirname(__file__)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(PROJECT_ROOT, 'db.sqlite3')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

APPS_ROOT = os.path.join(PROJECT_ROOT, 'src')
sys.path.insert(0, APPS_ROOT)

APPEND_SLASH=True

DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H:i'

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
PHOTOS_ROOT = os.path.join(MEDIA_ROOT, 'photos')

SECRET_KEY = '6vtp6va=kwegt$@^j755a3oce^#3sm5%zq%fi8g96t)l5ctq%^'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',

    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
#    'cms.middleware.multilingual.MultilingualURLMiddleware',
#    'core.middleware.PortalMiddleware',
#    'django.middleware.csrf.CsrfResponseMiddleware',
)


ROOT_URLCONF = 'ratings.urls'

AUTHENTICATION_BACKENDS = (
    'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Should users be created when new OpenIDs are used to log in?
OPENID_CREATE_USERS = True

# When logging in again, should we overwrite user details based on
# data received via Simple Registration?
OPENID_UPDATE_DETAILS_FROM_SREG = True

# If set, always use this as the identity URL rather than asking the
# user.  This only makes sense if it is a server URL.
#OPENID_SSO_SERVER_URL = 'https://login.launchpad.net/'

# Tell django.contrib.auth to use the OpenID signin URLs.
LOGIN_URL = '/openid/login/'
LOGIN_REDIRECT_URL = '/'

# Should django_auth_openid be used to sign into the admin interface?
OPENID_USE_AS_ADMIN_LOGIN = False

#CUSTOM_USER_MODEL = 'core.accounts.Profile'

YA_FEEDS = (
	"http://blogs.yandex.ru/entriesapi/",
)

TEMPLATE_DIRS = (
	os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "cms.context_processors.media",
)

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
	'sorl.thumbnail',
	'cms',
	'publisher',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.file',
    'cms.plugins.flash',
    'cms.plugins.link',
#    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'cms.plugins.teaser',
    'cms.plugins.video',

	'mptt',
	'news',
	'django_openid_auth',
	'feeds',	
	'rating',
	'core',
	'graphic',
	'tinymce',
	'fts'
       
)

LANGUAGE_CODE = "ru"

_ = lambda s: s

LANGUAGES = (
    ('ru', _('Russian')),
#    ('es', _('Spain')),
#    ('en', _('English')),
)

CMS_LANGUAGE_CONF = {
    'ru':['en'],
#    'en':['ru'],
#    'es':['es'],
}

CMS_TEMPLATES = (
    ('base.html', _('default')),
)

CMS_SOFTROOT = True
CMS_MODERATOR = False
CMS_PERMISSION = False
CMS_REDIRECTS = True
CMS_SEO_FIELDS = True
CMS_MENU_TITLE_OVERWRITE = True
CMS_HIDE_UNTRANSLATED = True
CMS_FLAT_URLS = False

CMS_TEMPLATE_INHERITANCE = True 

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace",
    'theme': "advanced",
'theme_advanced_toolbar_location' : "top",
	'theme_advanced_toolbar_align' : "left",
	'theme_advanced_buttons1' : "search,separator,undo,redo,separator,cut,copy,paste,separator,link,unlink,anchor,separator,tablecontrols,separator,hr",
	'theme_advanced_buttons2' : "styleselect,separator,bold,italic,underline,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,bullist,numlist,outdent,indent,separator,sub,sup,separator,forecolor,backcolor,separator,code",
	'theme_advanced_buttons3' : "",
	'auto_cleanup_word' : 'true',
}

FORCE_SCRIPT_NAME = ''
GOOGLE_MAPS_API_KEY = 'ABQIAAAAo_BekSQzbIM45E_VTSQzXRTB0WtQ7uMj5AxTt8-NRSydQqMDsBR_pFkppvVwy4m66Euv5AaEPF8Ccg'

try:
    from settings_local import *
except ImportError:
    pass
