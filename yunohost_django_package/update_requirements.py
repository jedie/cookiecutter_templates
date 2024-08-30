"""
    Update "yunohost_django_package" requirements
    Will be called by:

        .../cookiecutter_templates$ cli.py update-template-req
"""

import subprocess
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
    verbose_copy2(
        src=pkg_path / 'requirements.dev.txt',
        dst=template_path / 'requirements.dev.txt',
    )
    verbose_copy2(
        src=pkg_path / 'conf' / 'requirements.txt',
        dst=template_path / 'conf' / 'requirements.txt',
    )

    # Special case: Update the "install_python.py" file:
    try:
        verbose_check_call(
            sys.executable,
            'dev-cli.py',
            'test',
            'django_example_ynh.tests.test_install_python.IncludeInstallPythonTestCase.test_install_python_is_up2date',
            cwd=pkg_path,
            verbose=verbose,
            exit_on_error=False,
        )
    except subprocess.CalledProcessError:
        # It's okay that the unittest failed,
        # Then the "install_python.py" file is not up-to-date.
        pass

    # Always copy the file:
    verbose_copy2(
        src=pkg_path / 'conf' / 'install_python.py',
        dst=template_path / 'conf' / 'install_python.py',
    )


if __name__ == '__main__':
    main(verbose=True)
