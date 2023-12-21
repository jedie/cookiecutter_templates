import sys
from pathlib import Path

from bx_py_utils.path import assert_is_file

import managetemplates


BASE_PATH = Path(managetemplates.__file__).parent
PACKAGE_ROOT = BASE_PATH.parent

assert_is_file(PACKAGE_ROOT / 'pyproject.toml')  # Exists only in cloned git repo


CLI_EPILOG = 'Project Homepage: https://github.com/jedie/cookiecutter_templates'


# Only "prod" dependencies:
REQ_TXT_PATH = PACKAGE_ROOT / 'requirements.txt'
assert_is_file(REQ_TXT_PATH)

# dependencies + "dev"-optional-dependencies:
REQ_DEV_TXT_PATH = PACKAGE_ROOT / 'requirements.dev.txt'
assert_is_file(REQ_DEV_TXT_PATH)

# Path to checkout Cookiecutter template for running tests:
TEST_PATH = PACKAGE_ROOT / 'generated_templates'

ALL_TEMPLATES = (
    'managed-django-project',
    'pipenv-python',
    'piptools-python',
    'poetry-django-app',
    'poetry-python',
    'yunohost_django_package',
)

ALL_PACKAGES = tuple(
    entry.name for entry in sorted(PACKAGE_ROOT.iterdir()) if entry.is_dir() and Path(entry, '__init__.py').is_file()
)

UPDATE_TEMPLATE_REQ_FILENAME = 'update_requirements.py'


PY_BIN_PATH = Path(sys.executable).parent
