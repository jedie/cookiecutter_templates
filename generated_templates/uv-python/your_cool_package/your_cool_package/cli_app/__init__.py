"""
    CLI for usage
"""

import logging
import sys
from collections.abc import Sequence

from cli_base.autodiscover import import_all_files
from cli_base.cli_tools.version_info import print_version
from tyro.extras import SubcommandApp

import your_cool_package
from your_cool_package import constants


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
    project_name = 'your-cool-package'  # Enforce program name if pipx used
    print_version(module=your_cool_package, project_name=project_name)
    app.cli(
        prog=project_name,
        description=constants.CLI_EPILOG,
        use_underscores=False,  # use hyphens instead of underscores
        sort_subcommands=True,
        args=args,
    )
