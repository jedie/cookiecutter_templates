from pathlib import Path
from unittest import TestCase

import tomli
from bx_py_utils.path import assert_is_file

from managetemplates import __version__
from managetemplates.cli.cli_app import check_code_style, fix_code_style
from managetemplates.constants import PACKAGE_ROOT


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        assert_is_file(pyproject_toml_path)

        self.assertIsNotNone(__version__)

        pyproject_toml = tomli.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['project']['version']

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
