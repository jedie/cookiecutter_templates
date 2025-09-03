import logging

from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from managetemplates.cli_app import app
from managetemplates.cli_dev.annotations import TyroOptionalTemplateNameArgType
from managetemplates.constants import ALL_TEMPLATES
from managetemplates.utilities.reverse import reverse_test_project
from managetemplates.utilities.sync_cookiecutter_templates import (
    cookiecutter_templates2generated,
    update_cookiecutter_templates_requirements,
)


logger = logging.getLogger(__name__)


@app.command
def update_template_req(verbosity: TyroVerbosityArgType, template_name: TyroOptionalTemplateNameArgType):
    """
    Update requirements of all cookiecutter templates
    """
    update_cookiecutter_templates_requirements(verbosity=verbosity, only_template=template_name)


@app.command
def templates2generated(template_name: TyroOptionalTemplateNameArgType, force_recreate: bool = True):
    """
    Generate all cookiecutter templates
    """
    cookiecutter_templates2generated(force_recreate=force_recreate, only_template=template_name)


@app.command
def reverse(template_name: TyroOptionalTemplateNameArgType):
    """
    Reverse a /generated_templates/<pkg_name>/ back to Cookiecutter template in: ./<pkg_name>/

    Note: The reversed cookiecutter template files cannot be accepted 1-to-1.
    """
    for pkg_name in sorted(ALL_TEMPLATES):
        if template_name and template_name != pkg_name:
            continue

        reverse_test_project(pkg_name=pkg_name)
