from pathlib import Path

from bx_py_utils.path import assert_is_dir, assert_is_file

import managetemplates


PACKAGE_ROOT = Path(managetemplates.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT)
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')

REQ_IN_PATH = PACKAGE_ROOT / 'managetemplates' / 'requirements.in'
assert_is_file(REQ_IN_PATH)
REQ_TXT_PATH = REQ_IN_PATH.with_suffix('.txt')
