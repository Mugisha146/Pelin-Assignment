
from pathlib import Path
import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '_bs3b66ks+=k)6=+z_x4-u4(e!-^tcc7wdi^75*%qv$nd1xzt9'
# or Use
# SECRET_KEY = os.environ.get("DJANGO_SECRET")

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ValidationApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ValidationApp.middleware.LogMiddleware',
]

ROOT_URLCONF = 'ValidationProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ValidationProject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
# Log settings
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')  # Create a 'logs' directory in your project
os.makedirs(LOGGING_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'debug.log'),
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error.log'),
        },
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',  # Logstash server host
            'port': 5959,         # Logstash server port
            'version': 1,
            'message_type': 'django',
            'fqdn': False,
            'tags': ['django'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'logstash'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file', 'logstash'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Log user visits
LOGGING_MIDDLEWARE = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': ['file', 'logstash'],
    'loggers': {
        'django.request': {
            'handlers': ['file', 'logstash'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

if 'test' in sys.argv:
    # Don't log to logstash during tests
    LOGGING_MIDDLEWARE['handlers'] = ['file']

LOGGING['loggers'].update(LOGGING_MIDDLEWARE['loggers'])
