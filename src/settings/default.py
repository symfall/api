"""
Django settings for Symfall project.
"""

import logging
import os
from distutils.util import strtobool
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

PROJECT_NAME = "Symfall"

sentry_sdk.init(  # noqa
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s %(message)s",
        },
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s "
            "[%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        },
    },
    "root": {
        "level": logging.DEBUG,
        "handlers": ["console"],
    },
    "handlers": {
        "console": {
            "level": logging.DEBUG,
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": logging.DEBUG,
            "propagate": False,
        },
        "faker": {
            "handlers": ["console"],
            "level": logging.INFO,
        },
    },
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DEBUG", "False"))

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

# Turn on Clickjacking Protection
X_FRAME_OPTIONS = "DENY"
# sets the X-XSS-Protection: 1; mode=block header on all responses
SECURE_BROWSER_XSS_FILTER = True
# sets the X-Content-Type-Options: nosniff header on all responses
SECURE_CONTENT_TYPE_NOSNIFF = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    #
    "corsheaders",
    #
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.psutil",
    "health_check.contrib.migrations",
    #
    "django_extensions",
    #
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    #
    "channels",
    #
    "messenger",
    "authentication",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    #
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:3000",
]

ROOT_URLCONF = "urls"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.LimitOffsetPagination"
    ),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "PAGE_SIZE": 20,
}
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
}

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
]
MAX_FILE_SIZE_UPLOAD = 100 * 1024 * 1024

MEDIA_ROOT = BASE_DIR.parent / "media/"
MEDIA_URL = "/media/"

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = BASE_DIR.parent / "static/"
STATIC_URL = "/static/"

HEALTH_CHECK = {
    "DISK_USAGE_MAX": 90,
    "MEMORY_MIN": 100,
}

WSGI_APPLICATION = "server.wsgi.application"
ASGI_APPLICATION = "server.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (
                    os.getenv("CACHE_HOST", "redis"),
                    int(os.getenv("CACHE_PORT", "6379")),
                )
            ],
        },
    },
}

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

AUTH_USER_MODEL = "auth.User"  # pylint: disable=hard-coded-auth-user

# Database

DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DATABASE_ENGINE", "django.db.backends.postgresql"
        ),
        "NAME": os.getenv("DATABASE_NAME", "postgres"),
        "USER": os.getenv("DATABASE_USER", "postgres"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "postgres"),
        "HOST": os.getenv("DATABASE_HOST", "db"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = strtobool(os.getenv("EMAIL_USE_TLS", "True"))
EMAIL_HOST_USER = os.getenv("EMAIL_USER", "wrong-email@mail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD", "wrong-email-password")
