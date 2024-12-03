import logging

import click
from cli_base.cli_tools.dev_tools import run_unittest_cli
from cli_base.cli_tools.subprocess_utils import ToolsExecutor
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from cli_base.run_pip_audit import run_pip_audit
from manageprojects.utilities.publish import publish_package

import managetemplates
from managetemplates.cli_dev import PACKAGE_ROOT, cli


logger = logging.getLogger(__name__)


@cli.command()
def install():
    """
    Install requirements and 'managetemplates' via pip as editable.
    """
    tools_executor = ToolsExecutor(cwd=PACKAGE_ROOT)
    tools_executor.verbose_check_call('uv', 'sync')
    tools_executor.verbose_check_call('pip', 'install', '--no-deps', '-e', '.')


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def pip_audit(verbosity: int):
    """
    Run pip-audit check against current requirements files
    """
    setup_logging(verbosity=verbosity)
    run_pip_audit(base_path=PACKAGE_ROOT, verbosity=verbosity)


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def update(verbosity: int):
    """
    Update "requirements*.txt" dependencies files
    """
    setup_logging(verbosity=verbosity)

    tools_executor = ToolsExecutor(cwd=PACKAGE_ROOT)

    tools_executor.verbose_check_call('pip', 'install', '-U', 'pip')
    tools_executor.verbose_check_call('pip', 'install', '-U', 'uv')
    tools_executor.verbose_check_call('uv', 'lock', '--upgrade')

    run_pip_audit(base_path=PACKAGE_ROOT, verbosity=verbosity)

    # Install new dependencies in current .venv:
    tools_executor.verbose_check_call('uv', 'sync')

    # Update git pre-commit hooks:
    tools_executor.verbose_check_call('pre-commit', 'autoupdate')


@cli.command()
def publish():
    """
    Build and upload this project to PyPi
    """
    run_unittest_cli(verbose=False, exit_after_run=False)  # Don't publish a broken state

    publish_package(module=managetemplates, package_path=PACKAGE_ROOT)
