"""
Django settings for bepocart project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from datetime import datetime, timedelta
import os



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^hn!j!ra&i6p)52$-f0xmqpym%b8*&)+9k!hv5*#*rrc2ac31o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost","127.0.0.1","https://bepocart.in","*"]
CSRF_TRUSTED_ORIGINS = ["https://bepocart.in"]
APPEND_SLASH = False


CORS_ALLOW_CREDENTIALS = False

CORS_ALLOW_HEADERS = [
    'content-type',
    'accept',
    'authorization',
    'x-csrftoken',
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    "https://bepocart.in",
    "https://bepocart.com"
]

APPEND_SLASH = False

CORS_ALLOW_ALL_ORIGINS = True

SECURE_COOKIE = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'content-type',
    'accept',
    'authorization',
    'x-csrftoken',
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'bepocartAdmin',
    'bepocartBackend',
    'corsheaders',
    'storages',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'bepocart.urls'
# Django Rest Framework Simple JWT settings
# settings.py

# Your JWT settings
JWT_EXPIRATION_MINUTES = 144440  # Example expiration time

# Other Django settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Other Django settings


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bepocart.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databa


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bepocart',
        'USER': 'postgres',
        'PASSWORD': '252562',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'bepocart',
#         'USER': 'postgres',
#         'PASSWORD': '9645848527',
#         'HOST': 'database-1.c3qgaks0kpy9.eu-north-1.rds.amazonaws.com',
#         'PORT': '5432'
#     }
# }



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

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'bepocart.com'
EMAIL_PORT = 465  # Port for SMTP with SSL
EMAIL_USE_SSL = True  # Use SSL for SMTP
EMAIL_HOST_USER = 'contact@bepocart.com'
EMAIL_HOST_PASSWORD = 'haripriyaks@.com'

ADMIN_EMAIL = 'contact@bepocart.com'

RAZORPAY_KEY_ID = 'rzp_live_ZfYGbj0N5IPOBi'
RAZORPAY_KEY_SECRET = 'yu4HOaS7tK7zdmyHzK193K6w'


SMSALERT_API_KEY = '5e0741771f08e'


AWS_ACCESS_KEY_ID = 'AKIAQE3ROOKIXKPTB4F4'
AWS_SECRET_ACCESS_KEY = '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'

GOOGLE_CLIENT_ID = '517405395635-4tvq7b82kqpd97ba4ju6lk6gctdac1tk.apps.googleusercontent.com'


AWS_STORAGE_BUCKET_NAME = 'bepocart-bkt-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None  # Ensure public read access if needed

# Static files (CSS, JavaScript, Images)
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# Media files (uploaded files)
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Use S3 for storing static files
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Use S3 for storing media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB in bytes


SMSALERT_SENDER_ID = 1707162624534280862


FRONTEND_URL  =  'https://bepocart.com'
