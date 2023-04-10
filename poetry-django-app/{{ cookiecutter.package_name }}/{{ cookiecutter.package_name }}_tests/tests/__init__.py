from pathlib import Path
import os
import unittest.util

import {{ cookiecutter.package_name }}


# Hacky way to expand the failed test output:
unittest.util._MAX_LENGTH = os.environ.get('UNITTEST_MAX_LENGTH', 300)


PACKAGE_ROOT = Path({{ cookiecutter.package_name }}.__file__).parent.parent
