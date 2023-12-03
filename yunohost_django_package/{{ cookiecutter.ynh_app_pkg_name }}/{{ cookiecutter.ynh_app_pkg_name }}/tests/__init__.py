import os
import sys
import unittest.util
from pathlib import Path

import django
import {{ cookiecutter.ynh_app_pkg_name }}
from bx_py_utils.test_utils.deny_requests import deny_any_real_request
from cli_base.cli_tools.verbosity import MAX_LOG_LEVEL, setup_logging
from {{ cookiecutter.ynh_app_pkg_name }}.constants import PACKAGE_ROOT
from django_yunohost_integration.local_test import CreateResults, create_local_test
from rich import print  # noqa


def pre_configure_tests() -> None:
    print(f'Configure unittests via "load_tests Protocol" from {Path(__file__).relative_to(Path.cwd())}')

    # Hacky way to display more "assert"-Context in failing tests:
    _MIN_MAX_DIFF = unittest.util._MAX_LENGTH - unittest.util._MIN_DIFF_LEN
    unittest.util._MAX_LENGTH = int(os.environ.get('UNITTEST_MAX_LENGTH', 300))
    unittest.util._MIN_DIFF_LEN = unittest.util._MAX_LENGTH - _MIN_MAX_DIFF

    # Deny any request via docket/urllib3 because tests they should mock all requests:
    deny_any_real_request()

    # Display DEBUG logs in tests:
    setup_logging(verbosity=MAX_LOG_LEVEL)


def setup_ynh_tests() -> None:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    print('Compile YunoHost files...')
    result: CreateResults = create_local_test(
        django_settings_path=PACKAGE_ROOT / 'conf' / 'settings.py',
        destination=PACKAGE_ROOT / 'local_test',
        runserver=False,
        extra_replacements={
            '__DEBUG_ENABLED__': '0',  # "1" or "0" string
            '__LOG_LEVEL__': 'INFO',
            '__ADMIN_EMAIL__': 'foo-bar@test.tld',
            '__DEFAULT_FROM_EMAIL__': 'django_app@test.tld',
        },
    )
    print('Local test files created:')
    print(result)

    data_dir = str(result.data_dir_path)
    if data_dir not in sys.path:
        sys.path.insert(0, data_dir)

    django.setup()

    os.chdir(Path({{ cookiecutter.ynh_app_pkg_name }}.__file__).parent)


def load_tests(loader, tests, pattern):
    """
    Use unittest "load_tests Protocol" as a hook to setup test environment before running tests.
    https://docs.python.org/3/library/unittest.html#load-tests-protocol
    """
    pre_configure_tests()
    return loader.discover(start_dir=Path(__file__).parent, pattern=pattern)
