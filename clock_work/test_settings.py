"""
Test Settings for Clock Work

Uses SQLite in-memory database for faster test execution.
"""
import os
from .settings import *

# Use SQLite for tests - much faster than PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {
            'NAME': ':memory:',
        },
    }
}

# Disable password hashers for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable logging during tests
LOGGING = {}

# Use a simple email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Celery settings for tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable debug
DEBUG = False

# Django 4.2+ STORAGES configuration (replaces DEFAULT_FILE_STORAGE)
# Remove the old setting from parent
if 'DEFAULT_FILE_STORAGE' in globals():
    del DEFAULT_FILE_STORAGE
if 'STATICFILES_STORAGE' in globals():
    del STATICFILES_STORAGE

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Disable deprecated warnings
USE_L10N = True  # Will be removed in Django 5.0

# Static files settings for tests
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Allow test hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'testserver']

# Disable security settings for tests
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
