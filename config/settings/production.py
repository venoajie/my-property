# config/settings/production.py

from .base import *
import environ

# ----- Initialization & Environment -----
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")  # Load before other settings

# ----- Security Enforcement -----
# Hardcoded values - REPLACE WITH ACTUAL DOMAIN IN PRODUCTION
SECURITY_DEFAULTS = {
    "ALLOWED_HOSTS": ["130.61.246.120", "localhost", "127.0.0.1"],  # Production domain placeholder
    "CSRF_TRUSTED_ORIGINS": ["https://130.61.246.120", "https://localhost"],  # HTTPS domains only
    "SECRET_MIN_LENGTH": 50  # Minimum required secret key length
}

# ----- Core Configuration -----
DEBUG = False
SECRET_KEY = env("SECRET_KEY")  # Must be set in environment

# ----- Host & Network Security -----
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=SECURITY_DEFAULTS["ALLOWED_HOSTS"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=SECURITY_DEFAULTS["CSRF_TRUSTED_ORIGINS"])

# ----- HTTPS & Cookie Security -----
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True  # Force HTTPS redirects
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SAMESITE = "Strict"

# ----- Security Headers -----
SECURE_HSTS_SECONDS = 31536000  # 1 year HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# ----- Monitoring & Metrics -----
INSTALLED_APPS += ['django_prometheus']

MIDDLEWARE = [
    # Monitoring first to capture entire request lifecycle
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    
    # Core security middleware
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    # Django core middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    
    # Rate limiting
    "django_ratelimit.middleware.RatelimitMiddleware",
    
    # Monitoring last to capture response metrics
    'django_prometheus.middleware.PrometheusAfterMiddleware'
] + MIDDLEWARE[6:]  # Preserve custom middleware

# ----- Database Configuration -----
DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.postgresql',  # Instrumented DB
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST", default="db"),
        'PORT': env("POSTGRES_PORT", default="5432"),
    }
}

# ----- Rate Limiting -----
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"  # Requires Redis
RATELIMIT_FAIL_OPEN = False  # Fail-secure if Redis down

# Environment-configured rates (set in .env)
RATELIMIT_GLOBAL = env("RATELIMIT_GLOBAL", default="100/h")
RATELIMIT_AUTH = env("RATELIMIT_AUTH", default="5/m")

# ----- Logging -----
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
            "maxBytes": 1024 * 1024 * 5,  # 5MB rotation
            "backupCount": 3,
            "formatter": "verbose",
            "delay": True,  # Defer file creation
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

# ----- Safety Checks -----
if DEBUG:
    raise RuntimeError("DEBUG must be False in production!")


if len(SECRET_KEY) < 50:
    raise ValueError("SECRET_KEY must be at least 50 characters!")