import sys
from pathlib import Path

from bx_py_utils.path import assert_is_file

import managetemplates


BASE_PATH = Path(managetemplates.__file__).parent

PACKAGE_ROOT = BASE_PATH.parent
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')  # Exists only in cloned git repo

README_PATH = PACKAGE_ROOT / 'README.md'
assert_is_file(README_PATH)

CLI_EPILOG = 'Project Homepage: https://github.com/jedie/cookiecutter_templates'


# Path to checkout Cookiecutter template for running tests:
TEST_PATH = PACKAGE_ROOT / 'generated_templates'

ALL_TEMPLATES = (
    'make-uv-python',
    'managed-django-project',
    'uv-python',
    'yunohost_django_package',
)

ALL_PACKAGES = tuple(
    entry.name for entry in sorted(PACKAGE_ROOT.iterdir()) if entry.is_dir() and Path(entry, '__init__.py').is_file()
)

UPDATE_TEMPLATE_REQ_FILENAME = 'update_requirements.py'


PY_BIN_PATH = Path(sys.executable).parent
