"""
Django settings for orrangeit project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wh$-$zfoml)odpioenc=grf!rvw89*#**)ko9k*hragidlw_r+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('ORRANGEIT_DEBUG', True))

if DEBUG:
	ALLOWED_HOSTS = []
	SECRET_KEY = '(^bvf47lc+06+v+rul45ch(u!a1(&*p16a$vk#okso%thze6$z'
else:
	ALLOWED_HOSTS = ['127.0.0.1', 'orrangeit.me']
	SECRET_KEY = os.environ.get("ORRANGEIT_SECRET_KEY", 'SUPER SECRET KEY')


# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'tempus_dominus',
    'orrangeit_app.apps.OrrangeitAppConfig'
]

TEMPUS_DOMINUS_INCLUDE_ASSETS = True

ASGI_APPLICATION = 'orrangeit.routing.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'orrangeit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'orrangeit.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get("MARKET_MYSQL_DATABASE", 'define me'),
            'USER': os.environ.get("MARKET_MYSQL_USER", 'define me'),
            'PASSWORD': os.environ.get("MARKET_MYSQL_PASSWORD", 'define me'),
            'HOST': os.environ.get("MARKET_MYSQL_HOST", 'localhost'),
            'PORT': os.environ.get("MARKET_MYSQL_PORT", '3306'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticroot/'

MEDIA_URL = '/media/'
MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'media')
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_URL = '/'

LOGIN_REDIRECT_URL = 'index'

LOGOUT_REDIRECT_URL = 'index'

# убрать на релизе (нужно, чтобы письма появлялись в консоли, и не было ошибки о спаме)
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'support@orrangeit.me'
EMAIL_HOST_PASSWORD = 'PromProg1337'
DEFAULT_FROM_EMAIL = 'support@orrangeit.me'
EMAIL_USE_TLS = True

AUTH_USER_MODEL = 'orrangeit_app.User'


