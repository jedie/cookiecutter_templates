import subprocess
from importlib.metadata import version
from pathlib import Path
from unittest import TestCase

from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from packaging.version import Version

import {{ cookiecutter.package_name }}

PACKAGE_ROOT = Path({{ cookiecutter.package_name }}.__file__).parent.parent


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        # We get a version string:
        {{ cookiecutter.package_name }}_version_str = version('{{ cookiecutter.package_name }}')
        self.assertIsInstance({{ cookiecutter.package_name }}_version_str, str)
        self.assertTrue({{ cookiecutter.package_name }}_version_str)

        # Note: The actual installed version may be different from the one in the __init__.py file.
        # So check this too:
        self.assertIsInstance({{ cookiecutter.package_name }}.__version__, str)
        {{ cookiecutter.package_name }}_version = Version({{ cookiecutter.package_name }}.__version__)
        self.assertIsInstance({{ cookiecutter.package_name }}_version, Version)
        self.assertEqual(str({{ cookiecutter.package_name }}_version), {{ cookiecutter.package_name }}.__version__)  # Don't allow wrong formatting

    def test_code_style(self):
        try:
            output = subprocess.check_output(['make', 'lint'], stderr=subprocess.STDOUT, cwd=PACKAGE_ROOT, text=True)
        except subprocess.CalledProcessError:
            # Code style is not correct -> Try to fix it
            subprocess.check_call(['make', 'fix-code-style'], stderr=subprocess.STDOUT, cwd=PACKAGE_ROOT)

            # Check again:
            subprocess.check_call(['make', 'lint'], cwd=PACKAGE_ROOT)
        else:
            self.assertIn('darker', output)
            self.assertIn('flake8', output)

    def test_check_editor_config(self):
        check_editor_config(package_root=PACKAGE_ROOT)

        max_line_length = get_py_max_line_length(package_root=PACKAGE_ROOT)
        self.assertEqual(max_line_length, 119)
