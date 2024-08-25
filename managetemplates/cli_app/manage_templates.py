import logging

import rich_click as click
from cli_base.click_defaults import OPTION_ARGS_DEFAULT_FALSE, OPTION_ARGS_DEFAULT_TRUE
from rich import print  # noqa

from managetemplates import constants
from managetemplates.cli_app import cli
from managetemplates.constants import ALL_TEMPLATES
from managetemplates.utilities.reverse import reverse_test_project
from managetemplates.utilities.sync_cookiecutter_templates import (
    cookiecutter_templates2generated,
    update_cookiecutter_templates_requirements,
)


logger = logging.getLogger(__name__)


@cli.command()
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
@click.option(
    '--template-name',
    type=click.Choice(constants.ALL_PACKAGES, case_sensitive=False),
    required=False,
)
def update_template_req(verbose: bool, template_name: str | None):
    """
    Update requirements of all cookiecutter templates
    """
    update_cookiecutter_templates_requirements(verbose=verbose, only_template=template_name)


@cli.command()
@click.option('--force-recreate/--no-force-recreate', **OPTION_ARGS_DEFAULT_TRUE)
@click.option(
    '--template-name',
    type=click.Choice(constants.ALL_PACKAGES, case_sensitive=False),
    required=False,
)
def templates2generated(force_recreate: bool, template_name: str | None):
    """
    Generate all cookiecutter templates
    """
    cookiecutter_templates2generated(force_recreate=force_recreate, only_template=template_name)


@cli.command()
@click.option(
    '--template-name',
    type=click.Choice(constants.ALL_PACKAGES, case_sensitive=False),
    required=False,
)
def reverse(template_name: str | None):
    """
    Reverse a /generated_templates/<pkg_name>/ back to Cookiecutter template in: ./<pkg_name>/

    Note: The reversed cookiecutter template files cannot be accepted 1-to-1.
    """
    for pkg_name in sorted(ALL_TEMPLATES):
        if template_name and template_name != pkg_name:
            continue

        print('_' * 100)
        print(pkg_name)
        reverse_test_project(pkg_name=pkg_name)
