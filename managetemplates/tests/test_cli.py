from cli_base.cli_tools.test_utils.rich_test_utils import NoColorRichClickCli
from manageprojects.tests.base import BaseTestCase

from managetemplates import __version__, constants


class DevCliTestCase(BaseTestCase):

    def test_install(self):
        with NoColorRichClickCli() as cm:
            output = cm.invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('install',))
        self.assert_in_content(
            got=output,
            parts=(
                'pip install --no-deps -e .',
                f'Successfully installed managetemplates-{__version__}',
            ),
        )

    def test_pass_tox_command(self):
        with NoColorRichClickCli() as cm:
            output = cm.invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('tox', '--help'))
        self.assert_in_content(
            got=output,
            parts=(
                'usage: tox [-h] ',
                'list environments',
            ),
        )
        with NoColorRichClickCli() as cm:
            output = cm.invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('tox', 'list'))
        self.assert_in_content(
            got=output,
            parts=(
                'default environments:',
                'py311',
                'py310',
            ),
        )

    def test_pass_unittest_command(self):
        with NoColorRichClickCli() as cm:
            output = cm.invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('test', '--help'))
        self.assert_in_content(
            got=output,
            parts=(
                'usage: python -m unittest [-h] ',
                '--failfast',
                '--locals',
                '--buffer',
            ),
        )
