import subprocess
from pathlib import Path
from unittest import TestCase

import tomli
from bx_py_utils.path import assert_is_file

import {{ cookiecutter.package_name }}
from {{ cookiecutter.package_name }} import __version__
from {{ cookiecutter.package_name }}.cli import check_code_style, fix_code_style, mypy


PACKAGE_ROOT = Path({{ cookiecutter.package_name }}.__file__).parent.parent


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        assert_is_file(pyproject_toml_path)

        self.assertIsNotNone(__version__)

        pyproject_toml = tomli.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['tool']['poetry']['version']

        self.assertEqual(__version__, pyproject_version)

    def test_code_style(self):
        try:
            fix_code_style()
        except SystemExit as err:
            self.assertEqual(err.code, 0)
        else:
            raise AssertionError('No sys.exit() !')

        try:
            check_code_style(verbose=False)
        except SystemExit as err:
            self.assertEqual(err.code, 0)
        else:
            raise AssertionError('No sys.exit() !')

    def test_mypy(self):
        mypy(verbose=False)

    def test_poetry_check(self):
        output = subprocess.check_output(['poetry', 'check'], cwd=PACKAGE_ROOT, text=True)
        self.assertEqual(output, 'All set!\n')
