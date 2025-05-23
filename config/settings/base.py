# -*- coding: utf-8 -*-

from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for admin
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for admin
    'django.contrib.messages.middleware.MessageMiddleware',  # Required for admin
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add proper TEMPLATES configuration
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

# Add static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# Move all common settings here from original settings.py
# Update database config to use PostgreSQL
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///myproperty')
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Update media/config for S3
#AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
#AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'