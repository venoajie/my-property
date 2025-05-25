# config/settings/development.py
"""
Development Configuration

Purpose:
- Local development environment overrides
- Debugging tools enablement
- Relaxed security for development workflow

Security Considerations:
- NEVER deploy with these settings to production
- Debug mode exposes sensitive information
- Use separate credentials from production
"""

from .base import *  # noqa: F403, F401
from typing import List

# --- Core Development Settings ---
DEBUG: bool = True  # HARDCODED: Disable in production
ENVIRONMENT: str = "development"

# --- Host Configuration ---
# HARDCODED: Restrict to localhost in development
ALLOWED_HOSTS: List[str] = env.list("ALLOWED_HOSTS", default=[]) + [  # type: ignore
    '127.0.0.1',
    'localhost',
    '0.0.0.0'
]

# --- CSRF Configuration ---
# HARDCODED: Allow local development origins
CSRF_TRUSTED_ORIGINS: List[str] = env.list("CSRF_TRUSTED_ORIGINS", default=[]) + [  # type: ignore
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]

# --- Debug Toolbar Configuration ---
if DEBUG and "debug_toolbar" not in INSTALLED_APPS:  # type: ignore
    INSTALLED_APPS += ["debug_toolbar"]  # type: ignore
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # type: ignore
    INTERNAL_IPS: List[str] = ["127.0.0.1"]

# --- Development Security Settings ---
# WARNING: These reduce security for development convenience
SESSION_COOKIE_SECURE: bool = False
CSRF_COOKIE_SECURE: bool = False
SECURE_SSL_REDIRECT: bool = False

# --- Database Configuration ---
# Use SQLite for simpler local development
DATABASES["default"] = env.db(  # type: ignore
    "DATABASE_URL",
    default="sqlite:///" + str(BASE_DIR / "db.sqlite3")  # type: ignore
)

# --- Email Configuration ---
EMAIL_BACKEND: str = "django.core.mail.backends.console.EmailBackend"

# --- Logging Configuration ---
LOGGING["loggers"]["django"]["level"] = "DEBUG"  # type: ignore
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # type: ignore

# --- Development Tools ---
try:
    import django_extensions  # noqa: F401
    INSTALLED_APPS += ["django_extensions"]  # type: ignore
except ImportError:
    pass

def validate_development_settings() -> None:
    """Ensure development environment safety checks"""
    if not DEBUG:
        raise ImproperlyConfigured("Debug mode must be True in development")
    
    if SECRET_KEY == "dummy-key":  # type: ignore
        print("WARNING: Using insecure dummy secret key - set SECRET_KEY in .env")

validate_development_settings()