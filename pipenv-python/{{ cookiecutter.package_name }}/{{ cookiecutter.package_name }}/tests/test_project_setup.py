from pathlib import Path
from unittest import TestCase

try:
    import tomllib  # New in Python 3.11
except ImportError:
    import tomli as tomllib

from bx_py_utils.path import assert_is_file

import {{ cookiecutter.package_name }}
from {{ cookiecutter.package_name }} import __version__

PACKAGE_ROOT = Path({{ cookiecutter.package_name }}.__file__).parent.parent


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        assert_is_file(pyproject_toml_path)

        self.assertIsNotNone(__version__)

        pyproject_toml = tomllib.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['project']['version']

        self.assertEqual(__version__, pyproject_version)
