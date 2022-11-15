import subprocess
from pathlib import Path
from unittest import TestCase

import tomli
from bx_py_utils.path import assert_is_file

from managetemplates import __version__
from managetemplates.cli import PACKAGE_ROOT, check_code_style, fix_code_style


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        assert_is_file(pyproject_toml_path)

        self.assertIsNotNone(__version__)

        pyproject_toml = tomli.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['tool']['poetry']['version']

        self.assertEqual(__version__, pyproject_version)

    def test_poetry_check(self):
        output = subprocess.check_output(['poetry', 'check'], cwd=PACKAGE_ROOT, text=True)
        self.assertEqual(output, 'All set!\n')

    def test_code_style(self):
        fix_code_style()
        check_code_style(verbose=False)
