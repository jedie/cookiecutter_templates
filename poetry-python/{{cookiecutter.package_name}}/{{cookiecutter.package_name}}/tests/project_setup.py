from pathlib import Path
from unittest import TestCase
import tomli
from bx_py_utils.path import assert_is_file

from {{ cookiecutter.package_name }} import __version__


PACKAGE_ROOT = Path(__file__).parent.parent

class ProjectSetupTestCase(TestCase):

    def test_version(self):
        self.assertIsNotNone(__version__)

        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        assert_is_file(pyproject_toml_path)
        pyproject_toml = tomli.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['tool']['poetry']['version']

        self.assertEqual(__version__, pyproject_version)
