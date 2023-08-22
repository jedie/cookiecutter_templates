import os
import unittest.util
from pathlib import Path

import your_reuseable_django_app


# Hacky way to expand the failed test output:
unittest.util._MAX_LENGTH = os.environ.get('UNITTEST_MAX_LENGTH', 300)


PACKAGE_ROOT = Path(your_reuseable_django_app.__file__).parent.parent
