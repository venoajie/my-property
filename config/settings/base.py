# -*- coding: utf-8 -*-

from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

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