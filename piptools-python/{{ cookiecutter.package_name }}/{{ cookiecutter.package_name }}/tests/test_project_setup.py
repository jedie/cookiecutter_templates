from pathlib import Path
from unittest import TestCase

import tomli
import {{ cookiecutter.package_name }}
from bx_py_utils.path import assert_is_file
from {{ cookiecutter.package_name }} import __version__
from {{ cookiecutter.package_name }}.cli.cli_app import check_code_style, fix_code_style
from bx_py_utils.test_utils.redirect import RedirectOut


PACKAGE_ROOT = Path({{ cookiecutter.package_name }}.__file__).parent.parent
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        assert_is_file(pyproject_toml_path)

        self.assertIsNotNone(__version__)

        pyproject_toml = tomli.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['project']['version']

        self.assertEqual(__version__, pyproject_version)

    def test_code_style(self):
        with RedirectOut() as buffer:
            try:
                check_code_style(verbose=False)
            except SystemExit as err:
                if err.code == 0:
                    self.assertEqual(buffer.stderr, '')
                    stdout = buffer.stdout
                    self.assertIn('.venv/bin/darker', stdout)
                    self.assertIn('.venv/bin/flake8', stdout)
                    self.assertIn('Code style: OK', stdout)
                    return  # Code style is ok -> Nothing to fix ;)
            else:
                raise AssertionError('No sys.exit() !')

        # Try to "auto" fix code style:

        with RedirectOut() as buffer:
            try:
                fix_code_style(verbose=False)
            except SystemExit as err:
                self.assertEqual(err.code, 0, 'Code style can not be fixed, see output above!')
            else:
                raise AssertionError('No sys.exit() !')

        self.assertEqual(buffer.stderr, '')
        stdout = buffer.stdout
        self.assertIn('.venv/bin/darker', stdout)
        self.assertIn('Code style fixed, OK.', stdout)
