from pathlib import Path
from unittest import TestCase

from packaging.version import Version

import {{ cookiecutter.package_name }}
from {{ cookiecutter.package_name }} import __version__

PACKAGE_ROOT = Path({{ cookiecutter.package_name }}.__file__).parent.parent


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        self.assertIsNotNone(__version__)

        version = Version(__version__)  # Will raise InvalidVersion() if wrong formatted
        self.assertEqual(str(version), __version__)
