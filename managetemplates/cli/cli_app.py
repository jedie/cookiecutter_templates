# no:vars_cleanup

import logging
import sys
from pathlib import Path

import rich_click as click
from manageprojects.utilities import code_style
from manageprojects.utilities.publish import publish_package
from manageprojects.utilities.subprocess_utils import verbose_check_call
from manageprojects.utilities.version_info import print_version
from rich import print  # noqa
from rich_click import RichGroup

import managetemplates
from managetemplates import constants
from managetemplates.constants import PACKAGE_ROOT
from managetemplates.utilities.reverse import reverse_test_project
from managetemplates.utilities.sync_cookiecutter_templates import (
    cookiecutter_templates2generated,
    update_cookiecutter_templates_requirements,
)
from managetemplates.utilities.template_var_syntax import content_template_var_syntax, filesystem_template_var_syntax


logger = logging.getLogger(__name__)


OPTION_ARGS_DEFAULT_TRUE = dict(is_flag=True, show_default=True, default=True)
OPTION_ARGS_DEFAULT_FALSE = dict(is_flag=True, show_default=True, default=False)


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
@click.argument('package', type=click.Choice(constants.ALL_PACKAGES, case_sensitive=False), required=False)
@click.option(
    '--list',
    '-l',
    'list_packages',
    is_flag=True,
    show_default=True,
    default=False,
    help='Just list all packages (Copy&pasteable for github CI config)',
)
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def coverage(package=None, list_packages: bool = False, verbose: bool = True):
    """
    Run tests and show coverage.
    """
    if list_packages:
        print('Here the cureent package list, for github CI config matrix:')
        print(f'package: {list(constants.ALL_PACKAGES)}')
        sys.exit(0)

    args = [
        'coverage',
        'run',
    ]
    if package:
        print(f'\n[green]Run only tests from [yellow bold]{package}')
        args += [
            '-m',
            'unittest',
            '--verbose',
            '--locals',
            '--buffer',
            '-k',
            package,
        ]
    else:
        print('\n[green]Run all tests...')

    verbose_check_call(*args, verbose=verbose, exit_on_error=True, timeout=15 * 60)
    verbose_check_call('coverage', 'combine', '--append', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'report', '--fail-under=35', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'xml', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=True)


cli.add_command(coverage)


@click.command()
def install():
    """
    Run pip-sync and install 'managetemplates' via pip as editable.
    """
    verbose_check_call('pip-sync', constants.REQ_DEV_TXT_PATH)
    verbose_check_call('pip', 'install', '--no-deps', '-e', '.')


cli.add_command(install)


@click.command()
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def update(verbose: bool = False):
    """
    Update the development environment
    """
    bin_path = Path(sys.executable).parent

    verbose_check_call(bin_path / 'pip', 'install', '-U', 'pip')
    verbose_check_call(bin_path / 'pip', 'install', '-U', 'pip-tools')

    extra_env = dict(
        CUSTOM_COMPILE_COMMAND='./cli.py update',
    )

    pip_compile_base = [
        bin_path / 'pip-compile',
        '--allow-unsafe',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
        '--resolver=backtracking',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
        '--upgrade',
        '--generate-hashes',
    ]
    if verbose:
        pip_compile_base.append('--verbose')

    ############################################################################
    # Update own dependencies:

    # Only "prod" dependencies:
    verbose_check_call(
        *pip_compile_base,
        'pyproject.toml',
        '--output-file',
        constants.REQ_TXT_PATH,
        extra_env=extra_env,
    )
    # dependencies + "dev"-optional-dependencies:
    verbose_check_call(
        *pip_compile_base,
        'pyproject.toml',
        '--extra=tests',
        '--output-file',
        constants.REQ_DEV_TXT_PATH,
        extra_env=extra_env,
    )

    print('\nHint: Update templates requirements too!')
    print('Just call e.g.:')
    print('.../cookiecutter_templates$ cli.py update-template-req')


cli.add_command(update)


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
def publish():
    """
    Build and upload this project to PyPi
    """
    _run_unittest_cli(verbose=False, exit_after_run=False)  # Don't publish a broken state

    publish_package(
        module=managetemplates,
        package_path=PACKAGE_ROOT,
    )


cli.add_command(publish)


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
def templates2generated():
    """
    Generate all cookiecutter templates
    """
    cookiecutter_templates2generated()


cli.add_command(templates2generated)


@click.command()
@click.option('--color/--no-color', **OPTION_ARGS_DEFAULT_TRUE)
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def fix_code_style(color: bool = True, verbose: bool = False):
    """
    Fix code style via darker
    """
    code_style.fix(package_root=constants.PACKAGE_ROOT, color=color, verbose=verbose)


cli.add_command(fix_code_style)


@click.command()
@click.option('--color/--no-color', **OPTION_ARGS_DEFAULT_TRUE)
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def check_code_style(color: bool = True, verbose: bool = False):
    """
    Check code style by calling darker + flake8
    """
    code_style.check(package_root=constants.PACKAGE_ROOT, color=color, verbose=verbose)


cli.add_command(check_code_style)


@click.command()
@click.argument('pkg_name')
def reverse(pkg_name: str):
    """
    Reverse a /.tests/<pkg_name>/ back to Cookiecutter template in: ./<pkg_name>/
    """
    reverse_test_project(pkg_name=pkg_name)


cli.add_command(reverse)


@click.command()
def update_test_snapshot_files():
    """
    Update all test snapshot files (by remove and recreate all snapshot files)
    """

    def iter_snapshot_files():
        yield from PACKAGE_ROOT.rglob('*.snapshot.*')

    removed_file_count = 0
    for item in iter_snapshot_files():
        item.unlink()
        removed_file_count += 1
    print(f'{removed_file_count} test snapshot files removed... run tests...')

    # Just recreate them by running tests:
    _run_unittest_cli(
        extra_env=dict(
            RAISE_SNAPSHOT_ERRORS='0',  # Recreate snapshot files without error
        ),
        verbose=False,
        exit_after_run=False,
    )

    new_files = len(list(iter_snapshot_files()))
    print(f'{new_files} test snapshot files created, ok.\n')


cli.add_command(update_test_snapshot_files)


def _run_unittest_cli(extra_env=None, verbose=True, exit_after_run=True):
    """
    Call the origin unittest CLI and pass all args to it.
    """
    if extra_env is None:
        extra_env = dict()

    extra_env.update(
        dict(
            PYTHONUNBUFFERED='1',
            PYTHONWARNINGS='always',
        )
    )

    args = sys.argv[2:]
    if not args:
        if verbose:
            args = ('--verbose', '--locals', '--buffer')
        else:
            args = ('--locals', '--buffer')

    verbose_check_call(
        sys.executable,
        '-m',
        'unittest',
        *args,
        timeout=15 * 60,
        extra_env=extra_env,
    )
    if exit_after_run:
        sys.exit(0)


@click.command()  # Dummy command, to add "tests" into help page ;)
def test():
    """
    Run unittests
    """
    _run_unittest_cli()


cli.add_command(test)


def _run_tox():
    verbose_check_call(sys.executable, '-m', 'tox', *sys.argv[2:])
    sys.exit(0)


@click.command()  # Dummy "tox" command
def tox():
    """
    Run tox
    """
    _run_tox()


cli.add_command(tox)


def main():
    print_version(managetemplates)

    if len(sys.argv) >= 2:
        # Check if we just pass a command call
        command = sys.argv[1]
        if command == 'test':
            _run_unittest_cli()
        elif command == 'tox':
            _run_tox()

    # Execute Click CLI:
    cli.name = './cli.py'
    cli()
