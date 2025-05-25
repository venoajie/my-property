
# Create new settings file config/settings/build.py:
"""
Build-specific settings (no database required)
"""
from .production import *

# Disable database requirements for static collection
WHITENOISE_AUTOREFRESH = True
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'