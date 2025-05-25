# config/settings/production.py
from django.core.exceptions import ImproperlyConfigured
from .base import *
import environ
import os

# ----- Initialization -----
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")  # Load environment first

# ----- Core Configuration -----
DEBUG = False
SECRET_KEY = env("SECRET_KEY")  # Must be set in environment

# ----- Security Enforcement -----
# HARDCODED: Replace with actual domain in production
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["130.61.246.120", "localhost"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://130.61.246.120"])

# ----- HTTPS Configuration -----
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ----- Security Headers -----
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ----- Database -----
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST", default="db"),
        'PORT': env("POSTGRES_PORT", default="5432"),
    }
}

# ----- Middleware -----
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_ratelimit.middleware.RatelimitMiddleware",
]

# ----- Rate Limiting -----
RATELIMIT_ENABLE = True
RATELIMIT_VIEW = "apps.core.views.rate_limit_exceeded"

# ----- Logging -----
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join("/var/log/django", "app.log"),
            "maxBytes": 5 * 1024 * 1024,  # 5MB
            "backupCount": 3,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
        },
    },
}

# ----- Security Validation -----
if DEBUG:
    raise ImproperlyConfigured("DEBUG must be False in production!")

if len(SECRET_KEY) < 50:
    raise ValueError("SECRET_KEY must be at least 50 characters")

if any(origin.startswith("http://") for origin in CSRF_TRUSTED_ORIGINS):
    raise ImproperlyConfigured("Insecure origin in CSRF_TRUSTED_ORIGINS - use HTTPS")

# ----- AWS Configuration -----
# HARDCODED: Set AWS_S3_REGION_NAME in environment
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
AWS_QUERYSTRING_AUTH = False