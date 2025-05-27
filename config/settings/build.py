# config/settings/build.py
"""
Build-Specific Settings (Safe Minimal Configuration)

Security Purpose:
- Isolated environment for static asset compilation
- Zero production/database exposure during build
- Explicit app registration chain

Docker Integration:
- Matches Dockerfile's static collection path: /app/staticfiles
- Compatible with multi-stage build isolation
- Aligns with non-root user permissions

Maintenance Safety:
- Inherits ONLY required base settings
- Explicit app registration prevents leaks
- Disables all runtime features
"""

from .base import *  # noqa: F403

# Security: Disable all runtime integrations
DATABASES = {'default': {}}
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}

# Essential build apps only
INSTALLED_APPS = [
    # Core Django
    'django.contrib.staticfiles',
    
    # Project apps (explicit registration)
    'apps.core.apps.CoreConfig',
    'apps.users.apps.UsersConfig',
    'apps.listings.apps.ListingsConfig',
]

# Static files (matches Dockerfile paths)
STATIC_ROOT = '/app/staticfiles'
STATIC_URL = '/static/'

# Security: Disable all middleware
MIDDLEWARE = []

# Disable external integrations
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'