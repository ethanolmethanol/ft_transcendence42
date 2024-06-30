"""
Django settings for transcendence_django project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import subprocess
from corsheaders.defaults import default_headers
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-*6@dzmyjvs5+h)h1e)a!7rh*(u7%cb1g@zaad_p!a11n(k((zb"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "back_auth",
    "back_user",
    "back_game",
    "health_check",  # required
    "health_check.db",  # stock Django health checkers
    "health_check.cache",  # https://pypi.org/project/django-health-check/
    "health_check.storage",
    "health_check.contrib.migrations",
    "django_extensions",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "transcendence_django.urls"

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

WSGI_APPLICATION = "transcendence_django.wsgi.application"
ASGI_APPLICATION = "transcendence_django.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", ""),
        "USER": os.getenv("POSTGRES_USER", ""),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": "db",  # localhost
        "PORT": "5432",
    }
}

# AUTH_USER_MODEL = 'auth.User'

server_name = os.environ.get('HOSTNAME').lower()

print("Server name:", server_name)
print(f"Server name: https://{server_name}:4200")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

# CORS_ORIGIN_WHITELIST = [
#     "https://localhost:4200",
#     f"https://{server_name}:4200",
# ]

CORS_ALLOW_HEADERS = default_headers + (
    "CONTENT-TYPE",
    "X-CSRFToken",
)

ALLOWED_HOSTS = ["localhost", server_name]

CSRF_TRUSTED_ORIGINS = ("https://localhost:4200", f"https://{server_name}:4200", "http://localhost:1234")
CSRF_ALLOWED_ORIGINS = ["https://localhost:4200", f"https://{server_name}:4200", "http://localhost:1234"]
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

AUTHENTICATION_BACKENDS = ["back_auth.backends.EmailOrUsernameModelBackend"]
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

print("Database settings:")
print("Name:", DATABASES["default"]["NAME"])
print("User:", DATABASES["default"]["USER"])
print("Password:", DATABASES["default"]["PASSWORD"])
print("Host:", DATABASES["default"]["HOST"])
print("Port:", DATABASES["default"]["PORT"])

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'debug.log'),
#         },
#     },
#     'root': {
#         'handlers': ['console', 'file'],
#         'level': 'DEBUG',
#     },
# }
