# no:vars_cleanup

"""
    CLI for usage
"""
import logging
import sys
from pathlib import Path

import rich_click as click
from cli_base.cli_tools.version_info import print_version
from rich import print  # noqa
from rich.console import Console
from rich.traceback import install as rich_traceback_install
from rich_click import RichGroup

import managetemplates
from managetemplates import constants
from managetemplates.constants import ALL_TEMPLATES
from managetemplates.utilities.reverse import reverse_test_project
from managetemplates.utilities.sync_cookiecutter_templates import (
    cookiecutter_templates2generated,
    update_cookiecutter_templates_requirements,
)
from managetemplates.utilities.template_var_syntax import content_template_var_syntax, filesystem_template_var_syntax


logger = logging.getLogger(__name__)


OPTION_ARGS_DEFAULT_TRUE = dict(is_flag=True, show_default=True, default=True)
OPTION_ARGS_DEFAULT_FALSE = dict(is_flag=True, show_default=True, default=False)
ARGUMENT_EXISTING_DIR = dict(
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path)
)
ARGUMENT_NOT_EXISTING_DIR = dict(
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        readable=False,
        writable=True,
        path_type=Path,
    )
)
ARGUMENT_EXISTING_FILE = dict(
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, path_type=Path)
)


class ClickGroup(RichGroup):  # FIXME: How to set the "info_name" easier?
    def make_context(self, info_name, *args, **kwargs):
        info_name = './cli.py'
        return super().make_context(info_name, *args, **kwargs)


@click.group(
    cls=ClickGroup,
    epilog=constants.CLI_EPILOG,
)
def cli():
    pass


@click.command()
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def update_template_req(verbose: bool = False):
    """
    Update requirements of all cookiecutter templates
    """
    update_cookiecutter_templates_requirements(verbose)


cli.add_command(update_template_req)


@click.command()
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


cli.add_command(version)


@click.command()
def fix_filesystem():
    """
    Unify cookiecutter variables in the file/directory paths.
    e.g.: "/{{foo}}/{{bar}}.txt" -> "/{{ foo }}/{{ bar }}.txt"
    """
    rename_count = filesystem_template_var_syntax(path=constants.PACKAGE_ROOT)
    sys.exit(rename_count)


cli.add_command(fix_filesystem)


@click.command()
def fix_file_content():
    """
    Unify cookiecutter variables in file content.
    e.g.: "{{foo}}" -> "{{ foo }}"
    """
    fixed_files = content_template_var_syntax(path=constants.PACKAGE_ROOT)
    sys.exit(fixed_files)


cli.add_command(fix_file_content)


@click.command()
@click.option('--force-recreate/--no-force-recreate', **OPTION_ARGS_DEFAULT_TRUE)
@click.option('--template-name', type=click.Choice(constants.ALL_PACKAGES, case_sensitive=False), required=False)
def templates2generated(force_recreate: bool, template_name: str | None):
    """
    Generate all cookiecutter templates
    """
    cookiecutter_templates2generated(force_recreate=force_recreate, only_template=template_name)


cli.add_command(templates2generated)


@click.command()
@click.option('--template-name', type=click.Choice(constants.ALL_PACKAGES, case_sensitive=False), required=False)
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


cli.add_command(reverse)


def main():
    print_version(managetemplates)

    console = Console()
    rich_traceback_install(
        width=console.size.width,  # full terminal width
        show_locals=True,
        suppress=[click],
        max_frames=2,
    )

    # Execute Click CLI:
    cli.name = './cli.py'
    cli()
