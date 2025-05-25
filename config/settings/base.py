# config/settings/base.py
"""
Django base settings - inherited by environment-specific configurations
"""

from pathlib import Path
import os
import environ
from django.core.exceptions import ImproperlyConfigured

# --- Path Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project_root/config/settings/../../..

# --- Environment Setup ---
env = environ.Env()
try:
    env.read_env(BASE_DIR / ".env")  # Load .env first
except FileNotFoundError:
    pass  # Allow environment variables from other sources

# --- Core Configuration with Build Safety ---
try:
    SECRET_KEY = env("SECRET_KEY")
except ImproperlyConfigured:
    SECRET_KEY = 'dummy-key-for-build' if os.environ.get('IN_DOCKER_BUILD') else None

# --- Core Settings ---
DEBUG = env.bool("DEBUG", False)
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Security Settings ---
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"] if DEBUG else [])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# --- Application Definition ---
INSTALLED_APPS = [
    # Core Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Project apps
    "core.apps.CoreConfig",
    "listings.apps.ListingsConfig",
    "users.apps.UsersConfig",
]

# --- Middleware Stack ---
MIDDLEWARE = [
    # Security & infrastructure
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    # Core Django
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    
    # Security enhancements
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_ratelimit.middleware.RatelimitMiddleware",
]

# --- Database Configuration ---
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgresql:///myproperty?connect_timeout=10"
    )
}

# --- Template Configuration ---
TEMPLATES = [{
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
        "debug": env.bool("TEMPLATE_DEBUG", False),
    },
}]

# --- Static Files Configuration ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- Authentication ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Rate Limiting ---
RATELIMIT_VIEW = "core.views.rate_limit_exceeded"
RATELIMIT_RATE = env("RATELIMIT_RATE", default="100/m")
RATELIMIT_KEY = "header:x-forwarded-for" if not DEBUG else "ip"