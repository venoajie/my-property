# -*- coding: utf-8 -*-

from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = [os.environ.get('DOMAIN', '141.147.54.12')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': '5432',
    }
}

