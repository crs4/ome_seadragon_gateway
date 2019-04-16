"""
Django settings for ome_seadragon_gateway project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, yaml, sys
from yaml.scanner import ScannerError
from yaml.error import YAMLError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# load YAML configuration, look for
_CONF_FILE_PATH = os.environ.get('DJANGO_CONFIG_FILE',
                                 os.path.join(BASE_DIR, 'config', 'config.yaml'))
cfg = None
try:
    with open(_CONF_FILE_PATH, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
except (IOError, ScannerError, YAMLError):
    pass
if cfg is None:
    sys.exit('Config file not found')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = cfg['django']['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = cfg['django']['debug']

ALLOWED_HOSTS = cfg['django']['allowed_hosts']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'view_templates',
    'viewer_gw',
    'ome_data_gw',
    'ome_tags_gw',
    'static_files_gw',
    'examples',
    'oauth2_provider'
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ome_seadragon_gateway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ome_seadragon_gateway.wsgi.application'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Django logger
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s -- %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/ome_seadragon_gw.log',
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'ome_seadragon_gw': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

# Django REST Framework OAUTH2
OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope'}
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    )
}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if cfg['database']['engine'] == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, cfg['database']['name']),
        }
    }
elif cfg['database']['engine'] == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': cfg['database']['name'],
            'USER': cfg['database']['user'],
            'PASSWORD': cfg['database']['password'],
            'HOST': cfg['database']['host'],
            'PORT': cfg['database']['port']
        }
    }
else:
    sys.exit('A valid database engine should be provided, exit')


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = cfg['django']['static_root']

STATIC_URL = '/django/static/'

SESSION_COOKIE_NAME = cfg['django']['session_cookie']

CORS_ORIGIN_ALLOW_ALL = True

# CUSTOM SETTINGS
OMERO_COOKIE_NAME = cfg['omero']['cookie']

OME_USER = cfg['omero']['user']
OME_PASSWD = cfg['omero']['password']
OME_SERVER_ID = cfg['omero']['server_id']

OME_SEADRAGON_BASE_URL = cfg['ome_seadragon']['base_url']
OME_SEADRAGON_STATIC_FILES_URL = cfg['ome_seadragon']['static_files_url']

CACHE_SETTINGS = {
    'driver': cfg['cache']['driver'],
    'host': cfg['cache']['host'],
    'port': cfg['cache']['port'],
    'db': cfg['cache']['db'],
    'expire_time': cfg['cache']['expire_time']
}
