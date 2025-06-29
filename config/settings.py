"""
Django settings for the project.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from ast import literal_eval
from importlib.util import find_spec
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

# Environment
ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "production").lower()
BUILD = ENVIRONMENT == "build"
DEVELOPMENT = ENVIRONMENT == "development"
PRODUCTION = ENVIRONMENT == "production"
TESTING = ENVIRONMENT == "testing"
WORKER = ENVIRONMENT == "worker"
if not any((BUILD, DEVELOPMENT, PRODUCTION, TESTING, WORKER)):
    raise ImproperlyConfigured(
        "DJANGO_ENVIRONMENT must be set to one of the following: "
        "'build', 'development', 'production', 'testing' or 'worker'"
    )

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", None)
if SECRET_KEY is None and not BUILD:
    raise ImproperlyConfigured("SECRET_KEY must be set")

ALLOWED_HOSTS = literal_eval(
    os.getenv(
        "ALLOWED_HOSTS",
        "['localhost', '127.0.0.1']",
    )
)

# Trust the X-Forwarded-Proto header from our proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Use secure cookies unless explicitly set to false
SESSION_COOKIE_SECURE = not (
    os.getenv("SESSION_COOKIE_SECURE", "True").lower() == "false"
)

# Trust origins from ALLOWED_HOSTS unless a specific list is given
_csrf_trusted_origins_str = os.getenv("CSRF_TRUSTED_ORIGINS", None)

if _csrf_trusted_origins_str is not None:
    CSRF_TRUSTED_ORIGINS = literal_eval(_csrf_trusted_origins_str)
else:
    CSRF_TRUSTED_ORIGINS = [
        *[f"http://{host}:80" for host in ALLOWED_HOSTS],
        *[f"http://{host}:8000" for host in ALLOWED_HOSTS],
        *[f"https://{host}:443" for host in ALLOWED_HOSTS],
    ]


# Application definition

INSTALLED_APPS = [
    # Django apps:
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps:
    "channels",
    # Project apps:
    "examples",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


if DEVELOPMENT:
    INSTALLED_APPS = [
        "daphne",
        "django_browser_reload",
    ] + INSTALLED_APPS

    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]


if DEBUG and not TESTING and find_spec("debug_toolbar") is not None:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda _: True,
    }


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASE_URL = os.getenv("DATABASE_URL", None)

if DATABASE_URL is not None:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv(
                "DATABASE_ENGINE", "django.db.backends.sqlite3"
            ),
            "NAME": os.getenv("DATABASE_NAME", BASE_DIR / "db.sqlite3"),
            "HOST": os.getenv("DATABASE_HOST", None),
            "PORT": os.getenv("DATABASE_PORT", None),
            "USER": os.getenv("DATABASE_USER", None),
            "PASSWORD": os.getenv("DATABASE_PASSWORD", None),
        }
    }

DATABASES["default"].update(
    literal_eval(os.getenv("DATABASE_EXTRA_OPTIONS", "{}"))
)

# Cache and session store if CACHE_URL is provided (Redis-compatible)
CACHE_URL = os.getenv("CACHE_URL")
if CACHE_URL:
    # Cache
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": CACHE_URL,
        }
    }

    # Session
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
# Optionally via django-storages
# https://django-storages.readthedocs.io/en/latest/
USE_S3 = os.getenv("USE_S3", "False").lower() == "true"
if USE_S3:
    S3_ENDPOINT_URL = f"{os.getenv('S3_SCHEME', 'http')}://{
        os.getenv('S3_HOST', 's3')
    }:{os.getenv('S3_PORT', '3900')}"
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": os.getenv("S3_ACCESS_KEY_ID"),
                "secret_key": os.getenv("S3_SECRET_ACCESS_KEY"),
                "bucket_name": os.getenv(
                    "S3_STORAGE_BUCKET_NAME_MEDIA", "django-media"
                ),
                "endpoint_url": S3_ENDPOINT_URL,
                "region_name": os.getenv("S3_REGION_NAME"),
                "custom_domain": os.getenv("S3_CUSTOM_DOMAIN_MEDIA"),
                "url_protocol": os.getenv("S3_URL_PROTOCOL", "https:"),
                "default_acl": "public-read",
                "object_parameters": {
                    "CacheControl": "max-age=86400",
                },
                "querystring_auth": True,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": os.getenv("S3_ACCESS_KEY_ID"),
                "secret_key": os.getenv("S3_SECRET_ACCESS_KEY"),
                "bucket_name": os.getenv(
                    "S3_STORAGE_BUCKET_NAME_STATIC", "django-static"
                ),
                "endpoint_url": S3_ENDPOINT_URL,
                "region_name": os.getenv("S3_REGION_NAME"),
                "custom_domain": os.getenv("S3_CUSTOM_DOMAIN_STATIC"),
                "url_protocol": os.getenv("S3_URL_PROTOCOL", "https:"),
                "default_acl": "public-read",
                "object_parameters": {
                    "CacheControl": "max-age=31536000",
                },
                "querystring_auth": False,
            },
        },
    }

    # Media files
    if os.environ.get("S3_CUSTOM_DOMAIN"):
        domain = os.environ.get("S3_CUSTOM_DOMAIN")
        MEDIA_URL = f"http://{domain}/s3/media/"
        STATIC_URL = f"http://{domain}/django-static/"
    else:
        MEDIA_URL = "/s3/media/"
        STATIC_URL = "/s3/static/"
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    STATIC_URL = "static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"

    MEDIA_URL = "media/"
    MEDIA_ROOT = BASE_DIR / "media"

# Custom admin URL
ADMIN_PATH = os.getenv("DJANGO_ADMIN_PATH", "admin/")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
# https://docs.djangoproject.com/en/5.2/topics/auth/customizing/
AUTH_USER_MODEL = "users.User"

# Channels configuration (support for WebSockets and background workers)
# https://channels.readthedocs.io/en/latest/
CHANNEL_LAYERS = {
    "default": literal_eval(
        os.getenv(
            "CHANNEL_LAYER",
            "{'BACKEND': 'channels.layers.InMemoryChannelLayer'}",
        )
    )
}

# Health check setup
# https://django-health-check.readthedocs.io/en/latest/
USE_HEALTH_CHECK = os.getenv("USE_HEALTH_CHECK", "False").lower() == "true"
HEALTH_CHECK_PATH = os.getenv("HEALTH_CHECK_PATH", None)
if USE_HEALTH_CHECK:
    INSTALLED_APPS += [
        "health_check",
        "health_check.db",
        "health_check.contrib.migrations",
        "health_check.contrib.psutil",
    ]
    if CACHE_URL:
        INSTALLED_APPS += ["health_check.cache"]
    if USE_S3:
        INSTALLED_APPS += [
            "health_check.storage",
            "health_check.contrib.s3boto3_storage",
        ]
    HEALTH_CHECK = {
        "SUBSETS": {
            "liveness-probe": [],
        },
    }
    K8S_ADDRESS = os.getenv("WEB_SERVICE_HOST", None)
    if K8S_ADDRESS:
        ALLOWED_HOSTS.append(K8S_ADDRESS)
