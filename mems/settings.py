"""
Django settings for mems project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xj+1zl79!7fyf=&gw0($r4rycw6yr-4$0sskhqf!53)6$)l3ea'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['*', '*.ngrok-free.app', 'https://1276-105-163-1-222.ngrok-free.app']
ALLOWED_HOSTS = []

# CORS_ORIGIN_WHITELIST = [
#     'https://2fb8-105-163-1-222.ngrok-free.app',
#     '*',
#     '*.ngrok-free.app',
# ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'enterprise',
    'paypal.standard.ipn',
    'fontawesomefree'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mems.urls'

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

WSGI_APPLICATION = 'mems.wsgi.application'

AUTH_USER_MODEL = 'enterprise.User'

LOGOUT_REDIRECT_URL = 'client_login'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mems_backup',
        'USER': 'raga',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# media files
# ...

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# PAYPAL_RECEIVER_EMAIL = 'itsmraga@gmail.com'
PAYPAL_RECEIVER_EMAIL = 'sb-a4p8z26434210@business.example.com'

PAYPAL_TEST = True

# Email Settings
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

# EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PORT = 25
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'itsmraga@gmail.com'
EMAIL_HOST_PASSWORD = ''


DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# App name
# mems-prise

# PAYPAL_CLIENT_ID = 'AXSVJ5_sKOu49N0Hf5dfEU6tpTFbwGWPZQ7P4uq-2eoZrcyCEHxY9giJwE4b4-LJZq37wFHlt12VqLyV'
# AXSVJ5_sKOu49N0Hf5dfEU6tpTFbwGWPZQ7P4uq-2eoZrcyCEHxY9giJwE4b4-LJZq37wFHlt12VqLyV
# PAYPAL_CLIENT_SECRET = 'EGu0vXG_4Eq9jLtFa37L8IY3uvTA0HhaXmKUORnXtb41yUEfsE1F_09bdV62ehdnTr7of48o_N1bvyGL'
# EGu0vXG_4Eq9jLtFa37L8IY3uvTA0HhaXmKUORnXtb41yUEfsE1F_09bdV62ehdnTr7of48o_N1bvyGL
# PAYPAL_MODE = 'sandbox'  # 'sandbox' for testing, 'live' for production


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Sandbox URL
# https://sandbox.paypal.com

# Sandbox Region
# KE

# Email
# sb-a4p8z26434210@business.example.com

# Password
# AS4:<gDC
