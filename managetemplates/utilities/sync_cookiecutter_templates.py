from pathlib import Path
import sys

from bx_py_utils.path import assert_is_dir
from cli_base.cli_tools.rich_utils import EncloseRuleContext
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.tyro_commands import TyroVerbosityArgType
import django_example
from rich import print

from managetemplates.constants import ALL_TEMPLATES, PACKAGE_ROOT, UPDATE_TEMPLATE_REQ_FILENAME
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter


def cookiecutter_templates2generated(*, force_recreate: bool, only_template: str | None):
    if only_template:
        template_names = [only_template]
    else:
        template_names = sorted(ALL_TEMPLATES)

    for only_template in template_names:
        with EncloseRuleContext(f'templates2generated: {only_template!r}'):
            extra_context = {}
            if only_template == 'yunohost_django_package':
                extra_context = dict(
                    # Some projects test depends on the current upstream version
                    # So we have to set these version correct here:
                    upstream_version=django_example.__version__,
                )

            pkg_path: Path = run_cookiecutter(
                template_name=only_template,
                force_recreate=force_recreate,
                extra_context=extra_context,
            )
            print(pkg_path)

            if len(template_names) == 1:
                return pkg_path


def update_cookiecutter_templates_requirements(*, verbosity: TyroVerbosityArgType, only_template: str | None):
    if only_template:
        template_names = [only_template]
    else:
        template_names = sorted(ALL_TEMPLATES)

    for template_name in template_names:
        with EncloseRuleContext(f'Update requirements of {template_name!r}'):

            template_path = PACKAGE_ROOT / template_name
            assert_is_dir(template_path)

            update_req_path = template_path / UPDATE_TEMPLATE_REQ_FILENAME
            if not update_req_path.is_file():
                print(f'[red]ERROR: file not found: {update_req_path.relative_to(PACKAGE_ROOT)}')
            else:
                verbose_check_call(
                    sys.executable,
                    UPDATE_TEMPLATE_REQ_FILENAME,
                    cwd=template_path,
                    verbose=verbosity > 0,
                )
