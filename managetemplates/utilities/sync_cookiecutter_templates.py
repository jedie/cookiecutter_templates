import sys
from pathlib import Path

from bx_py_utils.path import assert_is_dir
from manageprojects.utilities.subprocess_utils import verbose_check_call
from rich import print

from managetemplates.constants import ALL_TEMPLATES, PACKAGE_ROOT, UPDATE_TEMPLATE_REQ_FILENAME
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter


def cookiecutter_templates2generated(force_recreate: bool = False) -> None:
    for template_name in sorted(ALL_TEMPLATES):
        print('_' * 100)
        print(template_name)
        pkg_path: Path = run_cookiecutter(
            template_name=template_name,
            force_recreate=force_recreate,
        )
        print(pkg_path)


def update_cookiecutter_templates_requirements(verbose: bool = False):
    for template_name in sorted(ALL_TEMPLATES):
        print('_' * 100)
        print(template_name)

        template_path = PACKAGE_ROOT / template_name
        assert_is_dir(template_path)

        update_req_path = template_path / UPDATE_TEMPLATE_REQ_FILENAME
        if not update_req_path.is_file():
            print(f'[red]ERROR: file not found: {update_req_path.relative_to(PACKAGE_ROOT)}')
            continue

        verbose_check_call(sys.executable, UPDATE_TEMPLATE_REQ_FILENAME, cwd=template_path, verbose=verbose)
