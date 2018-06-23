# -*- coding: utf-8 -*-

import libtorrent
import os

from decouple import config


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='4sl7-0#z5=2m#9#)7v9%eos^7jhoqh_)^z@4j1a_l=p(4(&%3k', cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'corsheaders',

    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flex.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'flex.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE', default='django.db.backends.sqlite3', cast=str),
        'HOST': config('DATABASE_HOST', default='localhost', cast=str),
        'NAME': config('DATABASE_NAME', default=os.path.join(BASE_DIR, 'db.sqlite3'), cast=str),
        'USER': config('DATABASE_USER', default='mylocaluser', cast=str),
        'PASSWORD': config('DATABASE_PASSWORD', default='mylocalpasswd', cast=str),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL[1:])


# Download root folder
ROOT_DOWNLOAD_FOLDER = '/Users/marcosfelipe/Movies'

CORS_ORIGIN_ALLOW_ALL = True


# Logging

if config('ENABLE_LOGGING', default=False, cast=bool):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
        },

        'formatters': {
            'verbose-pretty': {
                'format': '\n[%(levelname)s] (%(asctime)s) M:%(module)s P:%(process)d T:%(thread)d\n'
                          'Message: %(message)s',
                'datefmt': '%d/%m/%Y %H:%M:%S %z',
            },
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },

        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            }
        },

        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose-pretty'
            },
            'file-debug': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 16777216,  # 16MB
                'formatter': 'verbose-pretty',
                'filename': '/var/log/django/django-debug.log'
            },
            'file-errors': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 16777216,  # 16MB
                'formatter': 'verbose-pretty',
                'filename': '/var/log/django/django-errors.log'
            }
        },

        'loggers': {
            'django': {
                'level': 'DEBUG',
                'handlers': ['console', 'file-debug', 'file-errors'],
                'propagate': True,
            },
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console', 'file-errors'],
                'propagate': False,
            },
        },
    }
