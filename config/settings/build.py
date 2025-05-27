# config/settings/build.py  
"""  
Build Environment Configuration  

Security Features:  
- Isolated from production settings  
- Disabled database connections  
- Minimal app registry  
- Explicit static paths  

Docker Integration:  
- Matches /app/staticfiles in Dockerfile  
- Aligns with PYTHONPATH="/app:/app/apps:/app/config"  
- Compatible with non-root user permissions  
"""  

from .base import *  # noqa: F403  

# Security: Disable sensitive subsystems  
DATABASES = {'default': {}}  
SECRET_KEY = 'dummy-build-key'  # HARDCODED: Never use in production  

# Minimal app registry  
INSTALLED_APPS = [  
    # Core framework components  
    'django.contrib.staticfiles',  

    # Project apps (explicit registration)  
    'apps.core.apps.CoreConfig',  
    'apps.users.apps.UsersConfig',  
    'apps.listings.apps.ListingsConfig'  
]  

# Static assets configuration  
STATIC_ROOT = '/app/staticfiles'  # HARDCODED: Matches Dockerfile COPY  
STATIC_URL = '/static/'  

# Security: Disable all middleware  
MIDDLEWARE = []  