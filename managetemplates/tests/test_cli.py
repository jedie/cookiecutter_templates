from manageprojects.test_utils.click_cli_utils import subprocess_cli
from manageprojects.tests.base import BaseTestCase

from managetemplates import __version__, constants


class CliTestCase(BaseTestCase):

    def test_install(self):
        output = subprocess_cli(cli_bin=constants.PACKAGE_ROOT / 'cli.py', args=('install',))
        self.assert_in_content(
            got=output,
            parts=(
                'pip install --no-deps -e .',
                f'Successfully installed managetemplates-{__version__}',
            ),
        )

    def test_pass_tox_command(self):
        output = subprocess_cli(cli_bin=constants.PACKAGE_ROOT / 'cli.py', args=('tox', '--help'))
        self.assert_in_content(
            got=output,
            parts=(
                'usage: tox [-h] ',
                'list environments',
            ),
        )
        output = subprocess_cli(cli_bin=constants.PACKAGE_ROOT / 'cli.py', args=('tox', 'list'))
        self.assert_in_content(
            got=output,
            parts=(
                'default environments:',
                'py311',
                'py310',
            ),
        )

    def test_pass_unittest_command(self):
        output = subprocess_cli(cli_bin=constants.PACKAGE_ROOT / 'cli.py', args=('test', '--help'))
        self.assert_in_content(
            got=output,
            parts=(
                'usage: python -m unittest [-h] ',
                '--failfast',
                '--locals',
                '--buffer',
            ),
        )
