"""
    Update "make-uv-python" requirements
    Will be called by:

        .../cookiecutter_templates$ cli.py update-template-req
"""


from bx_py_utils.path import assert_is_dir
from cli_base.cli_tools.subprocess_utils import verbose_check_call

from managetemplates.constants import PACKAGE_ROOT
from managetemplates.utilities.verbose_copy import verbose_copy2


def main(verbose):
    pkg_path = PACKAGE_ROOT / 'generated_templates' / 'make-uv-python' / 'your_cool_package'
    assert_is_dir(pkg_path)

    verbose_check_call('make', 'update-requirements', cwd=pkg_path, verbose=verbose)

    # Sync the requirements back to the cookiecutter template:
    verbose_copy2(
        src=pkg_path / 'uv.lock',
        dst=PACKAGE_ROOT / 'make-uv-python' / '{{ cookiecutter.package_name }}' / 'uv.lock',
    )


if __name__ == '__main__':
    main(verbose=True)
