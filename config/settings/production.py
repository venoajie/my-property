# config/settings/production.py
"""
Production-specific settings for Django project

Security Considerations:
- All environment-sensitive values loaded from .env file
- Strict security headers enabled by default
- Production-specific checks and validations
"""

from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.utils.log import DEFAULT_LOGGING
from .base import *  # noqa: F403
import environ
import os

# --- Environment Initialization ---
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read .env file from project root (3 directories up from config/settings)
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    environ.Env.read_env(str(ENV_PATH))

# --- Core Configuration ---
DEBUG = False
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# --- Security Configuration ---
# HARDCODED WARNING: Replace default values with actual production domains
SECRET_KEY = env("SECRET_KEY")  # Must be 50+ characters
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["130.61.246.120", "localhost"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://130.61.246.120"])

# HTTPS Enforcement
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security Headers
SECURE_HSTS_SECONDS = 31536000  # 1 year - HARDCODED for maximum security
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# --- Database Configuration ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST", default="postgres-db"),  # Matches compose service name
        "PORT": env("POSTGRES_PORT", default="5432"),
        "CONN_MAX_AGE": 600,  # Enable persistent connections
    }
}

# --- Middleware Configuration ---
MIDDLEWARE = [
    # Security middleware first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
    
    # Core Django middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",  # Required for admin
    
    # Security middleware last
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_ratelimit.middleware.RatelimitMiddleware",
]

# --- Logging Configuration ---
LOG_DIR = Path("/var/log/django")
LOG_DIR.mkdir(exist_ok=True, parents=True)  # Ensure directory exists

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
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
            "maxBytes": 5 * 1024 * 1024,  # 5MB
            "backupCount": 3,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": True,
        },
        # Application-specific loggers
        "apps": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# --- Production Validation Checks ---
def validate_production_settings():
    """Enforce production security requirements"""
    if DEBUG:
        raise ImproperlyConfigured("DEBUG must be False in production!")

    if os.environ.get('IN_DOCKER_BUILD'):
        return  # Skip secret validation during build

    if len(SECRET_KEY) < 50:
        raise ValueError("SECRET_KEY must be at least 50 characters")

    # Validate CSRF origins
    insecure_origins = [
        origin for origin in CSRF_TRUSTED_ORIGINS
        if origin.startswith("http://") 
        and not origin.startswith(("http://localhost", "http://127.0.0.1"))
    ]
    if insecure_origins:
        raise ImproperlyConfigured(
            f"Insecure origins detected: {insecure_origins}. Use HTTPS for production domains"
        )

validate_production_settings()

# --- AWS Configuration (Commented for safety) ---
# HARDCODED: Uncomment and set these in environment for production
# AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
# AWS_QUERYSTRING_AUTH = False
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"