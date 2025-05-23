# -*- coding: utf-8 -*-

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['130.61.246.120', 'localhost', '127.0.0.1']  # Temporary for debugging
ALLOWED_HOSTS = ['*']  # Temporary for debugging

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE

# Configure static files storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECRET_KEY = os.environ.get('SECRET_KEY', 'dummy-key-for-dev-only')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}