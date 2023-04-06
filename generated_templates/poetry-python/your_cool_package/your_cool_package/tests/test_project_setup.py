import subprocess
from pathlib import Path
from unittest import TestCase


try:
    import tomllib  # New in Python 3.11
except ImportError:
    import tomli as tomllib

from bx_py_utils.path import assert_is_dir, assert_is_file
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from packaging.version import Version

import your_cool_package
from your_cool_package import __version__
from your_cool_package.cli import check_code_style, fix_code_style, mypy


PACKAGE_ROOT = Path(your_cool_package.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT)
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        assert_is_file(pyproject_toml_path)

        self.assertIsNotNone(__version__)

        version = Version(__version__)  # Will raise InvalidVersion() if wrong formatted
        self.assertEqual(str(version), __version__)

        pyproject_toml = tomllib.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['tool']['poetry']['version']

        self.assertEqual(__version__, pyproject_version)

        output = subprocess.check_output([PACKAGE_ROOT / 'cli.sh', 'version'], cwd=PACKAGE_ROOT, text=True)
        self.assertIn(f'your_cool_package v{__version__}', output)

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

    def test_check_editor_config(self):
        check_editor_config(package_root=PACKAGE_ROOT)

        max_line_length = get_py_max_line_length(package_root=PACKAGE_ROOT)
        self.assertEqual(max_line_length, 119)
