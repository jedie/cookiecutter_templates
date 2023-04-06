# flake8: noqa: E405
"""
    Settings used to run tests
"""
from your_cool_package_project.settings.prod import *  # noqa


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'No individual secret for tests ;)'

DEBUG = True

# Speedup tests by change the Password hasher:
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

# _____________________________________________________________________________

# Skip download map via geotiler in your_cool_package.gpx_tools.gpxpy2map.generate_map
MAP_DOWNLOAD = False


# All tests should use django-override-storage!
# Set root to not existing path, so that wrong tests will fail:
STATIC_ROOT = '/not/exists/static/'
MEDIA_ROOT = '/not/exists/media/'

# _____________________________________________________________________________
# Manage Django Project

INSTALLED_APPS.append('manage_django_project')
