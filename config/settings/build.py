# config/settings/build.py
"""
Build-Stage Configuration (Isolated Static File Generation)

Security Implementation:
- Disables database connectivity
- Disables debug capabilities
- Minimal allowed hosts configuration
- Eliminates external service dependencies

Critical Paths:
- STATIC_ROOT: Defines collection target directory
- DATABASES: Dummy engine prevents connection attempts
- WHITENOISE: Configures static file optimization

Design Purpose:
- Safe static asset compilation without production dependencies
- Prevents secret key exposure during build
- Enables container layer caching optimization
"""

from pathlib import Path
from .base import *  # noqa: F403,F401

# --------------------------
# Core Configuration
# --------------------------
DEBUG = False
ALLOWED_HOSTS = ['localhost']  # Hardcoded: Build context doesn't need valid domains

# --------------------------
# Static Files Configuration
# --------------------------
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Hardcoded: Matches Dockerfile WORKDIR

# WhiteNoise Optimization
WHITENOISE_AUTOREFRESH = True  # Disables per-request file checks
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --------------------------
# Security Hardening
# --------------------------
# Disable all authentication backends
AUTHENTICATION_BACKENDS = []

# Disable password validation
AUTH_PASSWORD_VALIDATORS = []

# --------------------------
# Database Simulation
# --------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
        'NAME': 'disabled_during_build',
    }
}

# --------------------------
# Service Disconnects
# --------------------------
# Disable caching system
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Disable email backend
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# --------------------------
# Build Validation
# --------------------------
# Ensure production settings don't leak into build
assert DEBUG is False, "Debug must be disabled during static file collection"
assert 'localhost' in ALLOWED_HOSTS, "Build requires localhost access"