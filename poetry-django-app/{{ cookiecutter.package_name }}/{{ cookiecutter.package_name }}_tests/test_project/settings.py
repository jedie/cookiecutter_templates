"""
    Django settings for {{ cookiecutter.package_name }} test project.
"""
import os
from pathlib import Path

import {{ cookiecutter.package_name }}


BASE_DIR = Path({{ cookiecutter.package_name }}.__file__).parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Only a test project!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    'debug_toolbar',
    #
    # Own Apps:
    '{{ cookiecutter.package_name }}.apps.AppConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{{ cookiecutter.package_name }}_tests.test_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{{ cookiecutter.package_name }}_tests.test_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
AUTH_PASSWORD_VALIDATORS = []  # Just a test project, so no restrictions


# Internationalization

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (BASE_DIR.parent / '{{ cookiecutter.package_name }}' / 'locale',)

TIME_ZONE = 'UTC'
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


INTERNAL_IPS = [
    '127.{{ cookiecutter.package_version }}',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {name} {module}.{funcName} {message}',
            'style': '{',
        },
    },
    'handlers': {'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'}},
    'loggers': {
        '': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'django.auth': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
        'django.security': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
        'django.request': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
        '{{ cookiecutter.package_name }}': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
    },
}


if os.environ.get('RAISE_LOG_OUTPUT') in ('1', 'true'):
    # Raise an error on every uncaptured log message
    LOGGING['handlers']['raise_error'] = {
        'class': 'bx_py_utils.test_utils.log_utils.RaiseLogUsage',
    }
    for logger_cfg in LOGGING['loggers'].values():
        logger_cfg['handlers'] = ['raise_error']
