import sys
from typing import Annotated

from cli_base.cli_tools.dev_tools import run_coverage, run_nox, run_unittest_cli
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.test_utils.snapshot import UpdateTestSnapshotFiles
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa
import tyro

from managetemplates import constants
from managetemplates.cli_dev import PACKAGE_ROOT, app
from managetemplates.cli_dev.annotations import TyroOptionalTemplateNameArgType


@app.command
def mypy(verbosity: TyroVerbosityArgType):
    """Run Mypy (configured in pyproject.toml)"""
    verbose_check_call('mypy', '.', cwd=PACKAGE_ROOT, verbose=verbosity > 0, exit_on_error=True)


@app.command
def update_test_snapshot_files(verbosity: TyroVerbosityArgType):
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


@app.command  # Dummy command
def test():
    """
    Run unittests
    """
    run_unittest_cli()


TyroListPackagesArgType = Annotated[
    bool,
    tyro.conf.arg(
        default=False,
        aliases=['-l', '--list'],
        help='Just list all packages (Copy&pasteable for github CI config)',
    ),
]


@app.command
def coverage(
    verbosity: TyroVerbosityArgType,
    list_packages: TyroListPackagesArgType,
    template_name: TyroOptionalTemplateNameArgType,
):
    """
    Run tests and show coverage.
    """
    setup_logging(verbosity=verbosity)

    if list_packages:
        print('Here the current package list, for github CI config matrix:')
        print(f'package: {list(constants.ALL_PACKAGES)}')
        sys.exit(0)

    if template_name:
        print(f'\n[green]Run only tests from [yellow bold]{template_name}')
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
            template_name,
        ]
    else:
        args = sys.argv
        print('\n[green]Run all tests...')

    run_coverage(argv=args, verbose=verbosity >= 1)


@app.command  # Dummy "nox" command
def nox():
    """
    Run nox
    """
    run_nox()
