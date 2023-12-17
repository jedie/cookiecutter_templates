from pathlib import Path

import {{ cookiecutter.ynh_app_pkg_name }}
from bx_py_utils.path import assert_is_file


PACKAGE_ROOT = Path({{ cookiecutter.ynh_app_pkg_name }}.__file__).parent.parent
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')


CLI_EPILOG = 'Project Homepage: {{ cookiecutter.ynh_app_url }}'
