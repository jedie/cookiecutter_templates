from cli_base.cli_tools.test_utils.rich_test_utils import NoColorRichClickCli, invoke
from manageprojects.tests.base import BaseTestCase

from managetemplates import __version__, constants


class DevCliTestCase(BaseTestCase):

    def test_install(self):
        with NoColorRichClickCli():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('install',))
        self.assert_in_content(
            got=output,
            parts=(
                'pip install --no-deps -e .',
                f'Successfully installed managetemplates-{__version__}',
            ),
        )

    def test_pass_tox_command(self):
        with NoColorRichClickCli():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('tox', '--help'))
        self.assert_in_content(
            got=output,
            parts=(
                'usage: tox [-h] ',
                'list environments',
            ),
        )
        with NoColorRichClickCli():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('tox', 'list'))
        self.assert_in_content(
            got=output,
            parts=(
                'default environments:',
                '3.13',
                '3.12',
            ),
        )

    def test_pass_unittest_command(self):
        with NoColorRichClickCli():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('test', '--help'))
        self.assert_in_content(
            got=output,
            parts=(
                'usage: python',  # Works with "python" and "python3" ;)
                ' -m unittest [-h] ',
                '--failfast',
                '--locals',
                '--buffer',
            ),
        )

    def test_coverage_help(self):
        with NoColorRichClickCli():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('coverage', '--help'))
        self.assert_in_content(
            got=output,
            parts=(
                '.venv/bin/managetemplates_dev coverage --help',
                './dev-cli.py coverage',
                ' --list ',
            ),
        )
