"""
    Update "managed-django-project" requirements
    Will be called by:

        .../cookiecutter_templates$ cli.py update-template-req
"""
import sys

from bx_py_utils.path import assert_is_dir
from cli_base.cli_tools.subprocess_utils import verbose_check_call

from managetemplates.constants import PACKAGE_ROOT
from managetemplates.utilities.verbose_copy import verbose_copy2


def main(verbose):
    pkg_path = PACKAGE_ROOT / 'generated_templates' / 'managed-django-project' / 'your_cool_package'
    assert_is_dir(pkg_path)

    verbose_check_call(sys.executable, 'manage.py', 'update_req', cwd=pkg_path, verbose=verbose)

    # Sync the requirements back to the cookiecutter template:
    print('_' * 100)
    for file_path in sorted(pkg_path.glob('requirements*.txt')):
        verbose_copy2(
            src=file_path,
            dst=PACKAGE_ROOT / 'managed-django-project' / '{{ cookiecutter.package_name }}' / file_path.name,
        )


if __name__ == '__main__':
    main(verbose=True)
