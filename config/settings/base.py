from pathlib import Path
import environ
import os

# ----- Path Configuration -----
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ----- Environment Setup -----
env = environ.Env()
env.read_env(BASE_DIR / ".env")  # Load before other settings

# ----- Core Settings -----
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", False)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ----- Security -----
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*' if DEBUG else 'localhost'])

CSRF_TRUSTED_ORIGINS = [
    origin.strip() 
    for origin in env.list("CSRF_TRUSTED_ORIGINS", default=[])
    if origin.startswith(('http://', 'https://'))
]
# ----- Database -----
DATABASES = {"default": env.db("DATABASE_URL", default="postgresql:///myproperty")}

TEST_RUNNER = "django.test.runner.DiscoverRunner"
TEST_DISCOVER_PATTERN = "test_*.py"

# ----- Applications -----
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "listings",  
    "users",
]

# ----- Middleware -----
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_ratelimit.middleware.RatelimitMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware", 
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----- Templates -----
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,  # Auto-discovery for app templates
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",  # Required for admin
            "django.contrib.auth.context_processors.auth",  # User context
            "django.contrib.messages.context_processors.messages",  # Messages
        ],
    },
}]

# ----- Static Files -----
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Production collection directory

# ----- Authentication -----
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ----- GDAL library ----- # currently irrelevant
# GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so'
# GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so'

RATELIMIT_VIEW = "apps.core.views.rate_limit_exceeded"  # Custom view
RATELIMIT_RATE = "5/m"  # Default rate: 5 requests/minute
RATELIMIT_KEY = "user_or_ip"  # Use both authenticated users and IP