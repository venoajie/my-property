# config/settings/production.py
"""
Production Configuration for Django Project

Security Implementation:
- Enforces HTTPS connections
- Strict Content Security Policies
- Security header protections
- Production database configuration
- Comprehensive logging setup

Critical Paths:
- ALLOWED_HOSTS: Defines valid domains (Must match Nginx config)
- CSRF_TRUSTED_ORIGINS: Approved request sources
- DATABASES: PostgreSQL connection settings
- LOGGING: Centralized logging configuration
"""

from pathlib import Path
import os
import environ
from django.core.exceptions import ImproperlyConfigured
from .base import *  # noqa: F403

# --- Environment Initialization ---
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables (3 directories up from config/settings)
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    environ.Env.read_env(str(ENV_PATH))

# --- Core Configuration ---
DEBUG = False
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# --- Security Configuration ---
# HARDCODED: Replace with production domain in .env
SECRET_KEY = env("SECRET_KEY")  # Must be 50+ characters
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["130.61.246.120", "localhost"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://130.61.246.120"])

# HTTPS Enforcement
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security Headers
SECURE_HSTS_SECONDS = 31536000  # 1 year - HARDCODED: Cannot be reduced once deployed
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Protect subdomains
SECURE_HSTS_PRELOAD = True  # Enable after submitting to HSTS preload list
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# --- Database Configuration ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),  # Matches compose service name
        "PORT": env("POSTGRES_PORT", default="5432"),
        "CONN_MAX_AGE": 600,  # Connection persistence
        "OPTIONS": {
            "sslmode": "require",  # Enforce SSL connections
            "connect_timeout": 5,  # 5 second connection timeout
        },
    }
}

# --- Middleware Stack ---
# Order is critical: Security first, utilities next, features last
MIDDLEWARE = [
    # Security & Infrastructure
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    # Core Request Processing
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    
    # Authentication & Authorization
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    
    # Security Enhancements
    "apps.core.middleware.BlockGitAccessMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_ratelimit.middleware.RatelimitMiddleware",
    
    # Monitoring & Diagnostics
    "django.middleware.common.BrokenLinkEmailsMiddleware",
]

# --- Logging Configuration ---
LOG_DIR = Path("/var/log/django")
LOG_DIR.mkdir(exist_ok=True, parents=True)  # Ensure log directory exists

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "security": {
            "format": "{asctime} {levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "app.log",
            "maxBytes": 5 * 1024 * 1024,  # 5MB per file
            "backupCount": 3,
            "formatter": "verbose",
        },
        "security_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "security.log",
            "maxBytes": 2 * 1024 * 1024,  # 2MB per file
            "backupCount": 5,
            "formatter": "security",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": True,
        },
        "apps.security": {
            "handlers": ["security_file"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# --- Production Validation ---
def validate_production_settings() -> None:
    """Enforce critical security requirements before startup"""
    if DEBUG:
        raise ImproperlyConfigured("DEBUG must be False in production!")

    if os.environ.get('IN_DOCKER_BUILD'):
        return  # Skip during container build

    # Secret key validation
    if len(SECRET_KEY) < 50:
        raise ValueError("SECRET_KEY must be ≥50 characters")

    # CSRF origin validation
    insecure_origins = [
        origin for origin in CSRF_TRUSTED_ORIGINS
        if origin.startswith("http://") 
        and not origin.startswith(("http://localhost", "http://127.0.0.1"))
]