# config/settings/production.py

from .base import *
import environ

# Initialization
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

# ------------------------ Core Security --------------------------
DEBUG = False
SECRET_KEY = env("SECRET_KEY")  # Must be set in environment

# ------------------------ Host Validation ------------------------
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "130.61.246.120",  # HARDCODED: Replace with production domain
        "localhost",
        "127.0.0.1"
    ]
)

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "https://130.61.246.120",  # HARDCODED: Use domain with HTTPS
        "https://localhost"
    ]
)

# ------------------------ HTTPS Enforcement ----------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SAMESITE = "Strict"

# ------------------------ Security Headers -----------------------
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

# ------------------------ Middleware -----------------------------
MIDDLEWARE = [
    # Security-focused middleware first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django_ratelimit.middleware.RatelimitMiddleware",
] + MIDDLEWARE[3:]  # Preserve remaining base middleware

# ------------------------ Static Files ---------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------ Rate Limiting --------------------------
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"  # Requires Redis configuration
RATELIMIT_FAIL_OPEN = False  # Block requests if Redis down

# Rate configurations (set in .env)
RATELIMIT_GLOBAL = env("RATELIMIT_GLOBAL", default="100/h")
RATELIMIT_AUTH = env("RATELIMIT_AUTH", default="5/m")

# ------------------------ Logging --------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/django/app.log",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 3,
            "formatter": "verbose",
            "delay": True, # Delay file creation until first write
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": env("DJANGO_LOG_LEVEL", default="WARNING"),
        },
        "django.security": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        }
    }
}

# ------------------------ Safety Checks --------------------------
if DEBUG:
    raise RuntimeError("DEBUG must be False in production!")

SECRET_KEY = 10

if len(SECRET_KEY) < SECRET_KEY:
    raise ValueError(f"SECRET_KEY must be at least {SECRET_KEY} characters!")