from pathlib import Path

from bx_py_utils.path import assert_is_dir, assert_is_file

import managetemplates


PACKAGE_ROOT = Path(managetemplates.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT)
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')

# Only "prod" dependencies:
REQ_TXT_PATH = PACKAGE_ROOT / 'managetemplates' / 'requirements.txt'
assert_is_file(REQ_TXT_PATH)

# dependencies + "dev"-optional-dependencies:
REQ_DEV_TXT_PATH = PACKAGE_ROOT / 'managetemplates' / 'requirements.dev.txt'
assert_is_file(REQ_DEV_TXT_PATH)

# Path to checkout Cookiecutter template for running tests:
TEST_PATH = PACKAGE_ROOT / '.tests'

ALL_TEMPLATES = (
    'pipenv-python',
    'piptools-python',
    'poetry-django-app',
    'poetry-python',
    'yunohost_django_package',
)
CLI_EPILOG = 'Project Homepage: https://github.com/jedie/cookiecutter_templates'
