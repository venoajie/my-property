from .base import *

DEBUG = False

# Add these lines
ALLOWED_HOSTS = ['141.147.54.12', 'localhost', '127.0.0.1']  # Temporary for debugging

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