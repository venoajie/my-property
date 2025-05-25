# config/settings/base.py
"""
Base Configuration for Django Project

Inherited By: development.py, production.py

Key Security Features:
- Environment-based secret management
- Content Security Policy foundation
- Secure database defaults
- Password validation rules
- Rate limiting foundation

Hardcoded Values:
- DEFAULT_AUTO_FIELD: Explicitly set for migration stability
- TEMPLATE_DEBUG: Default false fallback
- BLOCKED_PATH_PATTERNS: Common sensitive path patterns
"""

from pathlib import Path
import os
import environ
from django.core.exceptions import ImproperlyConfigured
from typing import List, Dict, Any

# --- Path Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project_root/config/settings/../../..
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# --- Environment Setup ---
env = environ.Env()
_ENV_FILE = BASE_DIR / ".env"

try:
    env.read_env(str(_ENV_FILE))  # type: ignore
except FileNotFoundError:
    pass  # Allow system environment variables

# --- Core Configuration ---
DEBUG: bool = env.bool("DEBUG", False)
SECRET_KEY: str = env("SECRET_KEY", default="dummy-key" if os.getenv("IN_DOCKER_BUILD") else None)  # type: ignore
DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"  # HARDCODED: Required for migration stability

# --- Security Configuration ---
ALLOWED_HOSTS: List[str] = env.list("ALLOWED_HOSTS", default=["*"] if DEBUG else [])
CSRF_TRUSTED_ORIGINS: List[str] = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF: bool = True  # HARDCODED: Critical security setting
X_FRAME_OPTIONS: str = "DENY"  # HARDCODED: Prevent clickjacking

# --- Application Definition ---
INSTALLED_APPS: List[str] = [
    # Core Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Project Apps
    "core.apps.CoreConfig",
    "listings.apps.ListingsConfig",
    "users.apps.UsersConfig",
]

# --- Middleware Stack ---
# Order Critical: Security first, features last
MIDDLEWARE: List[str] = [
    # Security & Infrastructure
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    # Core Request Processing
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    
    # Authentication
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    
    # Security Enhancements
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_ratelimit.middleware.RatelimitMiddleware",
]

# --- Database Configuration ---
# HARDCODED: SSL should be enabled in production override
_default_db_url: str = "postgresql:///myproperty?connect_timeout=10"
DATABASES: Dict[str, Dict[str, Any]] = {
    "default": env.db("DATABASE_URL", default=_default_db_url)
}

# --- Template Configuration ---
TEMPLATES: List[Dict[str, Any]] = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
        "debug": env.bool("TEMPLATE_DEBUG", False),  # HARDCODED: Default safety
    },
}]

# --- Static Files Configuration ---
STATIC_URL: str = "/static/"
STATIC_ROOT: Path = BASE_DIR / "staticfiles"
STATICFILES_STORAGE: str = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # HARDCODED: Optimized storage

# --- Path Security ---
BLOCKED_PATH_PATTERNS: List[str] = [
    r'\.git',  # Version control
    r'\.svn',  # Subversion
    r'\.env',  # Environment files
    r'~$',     # Temporary files
]

# --- Authentication ---
AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Rate Limiting ---
RATELIMIT_VIEW: str = "core.views.rate_limit_exceeded"  # HARDCODED: Path to custom view
RATELIMIT_RATE: str = env("RATELIMIT_RATE", default="100/m")  # Production override suggested
RATELIMIT_KEY: str = "header:x-forwarded-for" if not DEBUG else "ip"