from transcendence_django.settings import *

SECRET_KEY = "fake-key"

DEBUG = False

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#     }
# }

INSTALLED_APPS = [
    "tests",
    'django.contrib.contenttypes',
    'django.contrib.auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
]

MIDDLEWARE = [mw for mw in MIDDLEWARE if mw != 'django.middleware.csrf.CsrfViewMiddleware']

ALLOWED_HOSTS = ['*']

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

STATIC_URL = '/static/'

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
