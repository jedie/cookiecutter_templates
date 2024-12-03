"""
    Update "uv-python" requirements
    Will be called by:

        .../cookiecutter_templates$ cli.py update-template-req
"""
import sys

from bx_py_utils.path import assert_is_dir
from cli_base.cli_tools.subprocess_utils import verbose_check_call

from managetemplates.constants import PACKAGE_ROOT
from managetemplates.utilities.verbose_copy import verbose_copy2


def main(verbose):
    pkg_path = PACKAGE_ROOT / 'generated_templates' / 'uv-python' / 'your_cool_package'
    assert_is_dir(pkg_path)

    verbose_check_call(sys.executable, 'dev-cli.py', 'update', cwd=pkg_path, verbose=verbose)

    # Sync back to the cookiecutter template:
    for file_name in ('uv.lock', '.pre-commit-config.yaml'):
        verbose_copy2(
            src=pkg_path / file_name,
            dst=PACKAGE_ROOT / 'uv-python' / '{{ cookiecutter.package_name }}' / file_name,
        )


if __name__ == '__main__':
    main(verbose=True)
