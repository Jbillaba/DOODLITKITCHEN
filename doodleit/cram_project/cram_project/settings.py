"""
Django settings for cram_project project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from rest_framework.settings import api_settings
from dotenv import load_dotenv
from corsheaders.defaults import default_headers
import os

load_dotenv()

DJANGOKEY = os.getenv("SECRET_KEY")
DB_NAME = os.getenv("DATABASENAME")
DB_USER = os.getenv("DATABASEUSER")
DB_PASSWORD = os.getenv("DATABASEUSERPASS")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGOKEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("IN_DEBUG")



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'knox',
    'cram',
    'storages',
    'corsheaders',
    'django_extensions',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cram_project.urls'

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

WSGI_APPLICATION = 'cram_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD':DB_PASSWORD,
        'HOST':'localhost'
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/iamges/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_ROOT = BASE_DIR / '/static/images'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#DRF settings 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('cram.middleware.AuthFromCookie',),
}

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SAMESITE = "None"

CSRF_COOKIE_DOMAIN = "localhost"

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"

SESSION_COOKIE_DOMAIN = "localhost"

SESSION_COOKIE_SECURE = True

#S3 settings 
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_BUCKET")
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = os.getenv("AWS_REGION")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


#knox settings
REST_KNOX = {
    'SECURE_HASH_ALGORITHM':'hashlib.sha512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64, # By default, it is set to 64 characters (this shouldn't need changing).
    'TOKEN_TTL': timedelta(hours=12), # The default is 10 hours i.e., timedelta(hours=10)).
    'USER_SERIALIZER': 'knox.serializers.UserSerializer',
    'TOKEN_LIMIT_PER_USER': None, # By default, this option is disabled and set to None -- thus no limit.
    'AUTO_REFRESH': True, # This defines if the token expiry time is extended by TOKEN_TTL each time the token is used. 
    'MIN_REFRESH_INTERVAL': 120,
    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}

AUTH_USER_MODEL="cram.User"

#cors settings

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200'
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200'
]

#CACHE SETTINGS
CACHES={
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211"
    }
}

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'