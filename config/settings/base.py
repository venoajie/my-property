# config/settings/base.py
"""
Django base settings - inherited by environment-specific configurations
"""

from pathlib import Path
import environ

# --- Environment Setup ---
env = environ.Env()
env.read_env(BASE_DIR / ".env")  # Load .env first


# --- Core Configuration with Fallbacks ---
try:
    SECRET_KEY = env("SECRET_KEY")
except ImproperlyConfigured:
    SECRET_KEY = 'dummy-key-for-build' if os.environ.get('IN_DOCKER_BUILD') else None

# --- Path Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# --- Core Configuration ---
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", False)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Security Settings ---
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"] if DEBUG else ["localhost"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Security headers (enable in production)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# --- Application Definition ---
INSTALLED_APPS = [
    # Django core
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

# --- Middleware ---
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
    "django_ratelimit.middleware.RatelimitMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- Database ---
DATABASES = {"default": env.db("DATABASE_URL", default="postgresql:///myproperty")}  # Hardcoded fallback

# --- Templates ---
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
    },
}]

# --- Static Files ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- Authentication ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Rate Limiting ---
RATELIMIT_VIEW = "apps.core.views.rate_limit_exceeded"  # Hardcoded view path
RATELIMIT_RATE = "5/m"  # Should be environment-configurable
RATELIMIT_KEY = "user_or_ip"