from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.test_utils.snapshot import assert_text_snapshot
from manageprojects.test_utils.click_cli_utils import invoke_click, subprocess_cli
from manageprojects.tests.base import BaseTestCase

from managetemplates import __version__, constants
from managetemplates.cli.cli_app import cli


def assert_cli_help_in_readme(text_block: str, marker: str):
    text_block = text_block.replace(constants.CLI_EPILOG, '')
    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=constants.PACKAGE_ROOT / 'README.md',
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


class CliTestCase(BaseTestCase):
    def test_main_help(self):
        stdout = invoke_click(cli, '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...',
                'fix-file-content',
                'fix-filesystem',
                'reverse',
                constants.CLI_EPILOG,
            ),
        )
        assert_text_snapshot(got=stdout)
        assert_cli_help_in_readme(text_block=stdout, marker='main help')

    def test_install(self):
        output = subprocess_cli(cli_bin=constants.PACKAGE_ROOT / 'cli.py', args=('install',))
        self.assert_in_content(
            got=output,
            parts=(
                'pip install -e .',
                f'Successfully installed managetemplates-{__version__}',
            ),
        )
