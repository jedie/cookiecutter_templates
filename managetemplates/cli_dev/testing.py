import sys

import rich_click as click
from cli_base.cli_tools.dev_tools import run_coverage, run_tox, run_unittest_cli
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.test_utils.snapshot import UpdateTestSnapshotFiles
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging

from managetemplates import constants
from managetemplates.cli_dev import PACKAGE_ROOT, cli


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def mypy(verbosity: int):
    """Run Mypy (configured in pyproject.toml)"""
    verbose_check_call('mypy', '.', cwd=PACKAGE_ROOT, verbose=verbosity > 0, exit_on_error=True)


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def update_test_snapshot_files(verbosity: int):
    """
    Update all test snapshot files (by remove and recreate all snapshot files)
    """

    with UpdateTestSnapshotFiles(root_path=PACKAGE_ROOT, verbose=verbosity > 0):
        # Just recreate them by running tests:
        run_unittest_cli(
            extra_env=dict(
                RAISE_SNAPSHOT_ERRORS='0',  # Recreate snapshot files without error
            ),
            verbose=verbosity > 1,
            exit_after_run=False,
        )


@cli.command()  # Dummy command
def test():
    """
    Run unittests
    """
    run_unittest_cli()


@cli.command()
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
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def coverage(package=None, list_packages: bool = False, verbosity: int = 0):
    """
    Run tests and show coverage.
    """
    setup_logging(verbosity=verbosity)

    if list_packages:
        print('Here the current package list, for github CI config matrix:')
        print(f'package: {list(constants.ALL_PACKAGES)}')
        sys.exit(0)

    if package:
        print(f'\n[green]Run only tests from [yellow bold]{package}')
        args = [
            './dev-cli.py',
            'coverage',
            'run',
            '-m',
            'unittest',
            '--verbose',
            '--locals',
            '--buffer',
            '-k',
            package,
        ]
    else:
        args = sys.argv
        print('\n[green]Run all tests...')

    run_coverage(argv=args, verbose=verbosity >= 1)


@cli.command()  # Dummy "tox" command
def tox():
    """
    Run tox
    """
    run_tox()
