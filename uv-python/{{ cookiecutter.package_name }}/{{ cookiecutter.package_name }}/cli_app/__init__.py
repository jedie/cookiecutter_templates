"""
    CLI for usage
"""

import logging
import sys
from collections.abc import Sequence

from cli_base.autodiscover import import_all_files
from rich import print
from tyro.extras import SubcommandApp

from {{ cookiecutter.package_name }} import constants, __version__


logger = logging.getLogger(__name__)

app = SubcommandApp()

# Register all CLI commands, just by import all files in this package:
import_all_files(package=__package__, init_file=__file__)


@app.command
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


def main(args: Sequence[str] | None = None):
    prog = '{{ cookiecutter.project_name }}'  # Enforce program name if pipx used
    print(f'[bold][green]{prog}[/green] v{__version__}')
    app.cli(
        prog=prog,
        description=constants.CLI_EPILOG,
        use_underscores=False,  # use hyphens instead of underscores
        sort_subcommands=True,
        args=args,
    )
