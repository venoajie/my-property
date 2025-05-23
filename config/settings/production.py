
from .base import *

DEBUG = False
ALLOWED_HOSTS = [env('PRODUCTION_HOST', default='141.147.54.12')]
CSRF_TRUSTED_ORIGINS = [f'http://{host}' for host in ALLOWED_HOSTS]