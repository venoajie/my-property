from .base import *
import os

# ----- Core Overrides -----
DEBUG = False  # Never enable in production
CSRF_COOKIE_SECURE = True  # Only send CSRF cookie over HTTPS
SESSION_COOKIE_SECURE = True  # Only send session cookie over HTTPS

# ----- Host Configuration -----
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")  # Comma-separated list
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

# ----- Security Headers -----
SECURE_HSTS_SECONDS = 31536000  # 1 year HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ----- Middleware -----
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Before other middleware
] + MIDDLEWARE[1:]  # Preserve base middleware except SecurityMiddleware

# ----- Static Files -----
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ----- Secrets -----
SECRET_KEY = os.environ["SECRET_KEY"]  # No fallback in production
SECURE_SSL_REDIRECT = True  # Force HTTPS
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# ----- Logging -----
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


# Rate limiting security
RATELIMIT_RATE = "100/hour"  # Global default
RATELIMIT_ENABLE = True  # Enable in production
RATELIMIT_FAIL_OPEN = False  # Fail securely if Redis is down

# Environment-specific overrides
RATELIMIT_LOGIN_RATE = env("RATELIMIT_LOGIN_RATE", default="3/m")
RATELIMIT_API_RATE = env("RATELIMIT_API_RATE", default="100/h")