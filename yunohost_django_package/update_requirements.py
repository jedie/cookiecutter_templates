"""
    Update "yunohost_django_package" requirements
    Will be called by:

        .../cookiecutter_templates$ cli.py update-template-req
"""
import sys

from bx_py_utils.path import assert_is_dir
from cli_base.cli_tools.subprocess_utils import verbose_check_call

from managetemplates.constants import PACKAGE_ROOT
from managetemplates.utilities.verbose_copy import verbose_copy2


def main(verbose):
    pkg_path = PACKAGE_ROOT / 'generated_templates' / 'yunohost_django_package' / 'django_example_ynh'
    assert_is_dir(pkg_path)

    verbose_check_call(sys.executable, 'dev-cli.py', 'update', cwd=pkg_path, verbose=verbose)

    # Sync the requirements back to the cookiecutter template:
    template_path = PACKAGE_ROOT / 'yunohost_django_package' / '{{ cookiecutter.ynh_app_pkg_name }}'
    print('_' * 100)
    verbose_copy2(
        src=pkg_path / 'requirements.dev.txt',
        dst=template_path / 'requirements.dev.txt',
    )
    print('_' * 100)
    verbose_copy2(
        src=pkg_path / 'conf' / 'requirements.txt',
        dst=template_path / 'conf' / 'requirements.txt',
    )


if __name__ == '__main__':
    main(verbose=True)
