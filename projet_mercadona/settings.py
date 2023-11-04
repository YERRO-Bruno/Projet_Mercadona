"""
Django settings for projet_mercadona project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path
from imagekitio import ImageKit
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# IMAGEKIT Pictures server access key
IMAGEKIT_PUBLIC_KEY=config('IMAGEKIT_PUBLIC_KEY')
IMAGEKIT_PRIVATE_KEY=config('IMAGEKIT_PRIVATE_KEY')
IMAGEKIT_URL_ENDPOINT=config('IMAGEKIT_URL_ENDPOINT')
#SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG")
print(DEBUG)
if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS')
print(ALLOWED_HOSTS)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'mercadona.apps.MercadonaConfig',
    'rest_framework',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "projet_mercadona.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "projet_mercadona.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# if DEBUG:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "d43ghc8ldhtuhp",
        "USER": "psonfltbvpjftx",
        "PASSWORD": "0474b2280136144c4eb0b1b78daf13ff76f1b4a3dc49deca67a82e9a7900deeb",
        "HOST": "ec2-52-215-68-14.eu-west-1.compute.amazonaws.com",
        "PORT": "5432"
    }
}
# else:
#     DATABASE = os.getenv("DATABASE_URL")

AUTH_USER_MODEL = 'mercadona.User'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Emails

EMAIL_BACKEND = 'mercadona.mailing.CustomEmailBackend'
DEBUG_EMAIL = 'brunoyerro@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'brunoyerro@gmail.com'
EMAIL_HOST_PASSWORD = 'isti ynqp bvsa onvr'
EMAIL_USE_TLS = True