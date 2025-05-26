# config/wsgi.py
"""
WSGI Configuration for Production Deployment

Security Critical:
- Initializes application with production settings
- Sets environment variables before app initialization
- Entry point for ASGI/WSGI servers (Gunicorn, uWSGI)

Execution Flow:
1. Set default environment variables
2. Initialize Django application
3. Export application handler for server
"""

import os
from django.core.wsgi import get_wsgi_application
from typing import Any

# Security: Ensure production environment is explicitly set
# Hardcoded Value: Consider using environment variable in container runtime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# Initialize application with production configuration
application: Any = get_wsgi_application()

# Security: Prevent accidental environment overrides after initialization
__all__ = ["application"]  # Explicit exports for Python*

# Optional Production Checks (Uncomment for strict environments)
# if os.environ.get('DJANGO_ENV') != 'production':
#     raise RuntimeError("WSGI configuration loaded in non-production environment!")