"""
Django settings for chat project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
import django
from decouple import config
from django.conf import settings
import dj_database_url

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
#django.setup()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, "chat", "templates")

MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['shabd-chat.herokuapp.com','127.0.0.1','ec2-34-204-128-77.compute-1.amazonaws.com']  #change this


# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'corsheaders',
    'easy_thumbnails',
    'shabd',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'chat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'chat.wsgi.application'
ASGI_APPLICATION = 'chat.asgi.application'


# Database

DATABASES = {
 

#     'default': {

#         'ENGINE': 'django.db.backends.postgresql_psycopg2',

#         'NAME': '',

#         'USER': '',

#         'PASSWORD': config('password'),

#         'HOST': '',

#         'PORT': '',

#     }
 }

DATABASES['default'] = dj_database_url.config(conn_max_age=500)


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'

TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'chat', 'static'), )
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],

        },
    },
}

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (300, 300), 'crop': False,'quality':75},
    },
}
#THUMBNAIL_DEBUG = True


AUTH_USER_MODEL = 'shabd.CustomeUserProfile'
LOGIN_REDIRECT_URL = 'index'

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 
CORS_ORIGIN_ALLOW_ALL = True
CSRF_COOKIE_SECURE = True
LOGOUT_REDIRECT_URL='index' 

INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', 'localhost',)

#security settings

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True



