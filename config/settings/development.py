from .base import *

DEBUG = True
ALLOWED_HOSTS += ['127.0.0.1', 'localhost']
CSRF_TRUSTED_ORIGINS += ['http://localhost:8000']