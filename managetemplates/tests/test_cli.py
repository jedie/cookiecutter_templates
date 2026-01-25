from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich, invoke
from manageprojects.tests.base import BaseTestCase

from managetemplates import __version__, constants


class DevCliTestCase(BaseTestCase):

    def test_install(self):
        with NoColorEnvRich():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('install',))
        assert_in(
            content=output,
            parts=(
                'Built managetemplates',
                f'managetemplates=={__version__}',
            ),
        )

    def test_pass_nox_command(self):
        with NoColorEnvRich():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('nox', '--help'))
        assert_in(
            content=output,
            parts=(
                'managetemplates.cli_dev nox --help',
                'usage: nox [-h]',
                '--list-sessions',
            ),
        )
        with NoColorEnvRich():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('nox', '--list-sessions'))
        assert_in(
            content=output,
            parts=(
                '* tests-3.13',
                '* tests-3.12',
            ),
        )

    def test_pass_unittest_command(self):
        with NoColorEnvRich():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('test', '--help'))
        assert_in(
            content=output,
            parts=(
                'managetemplates.cli_dev test --help',
                ' -m unittest [-h] ',
                '--failfast',
                '--locals',
                '--buffer',
            ),
        )

    def test_coverage_help(self):
        with NoColorEnvRich():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('coverage', '--help'))
        assert_in(
            content=output,
            # Note: We use our custom coverage command, not the original!
            parts=(
                'managetemplates.cli_dev coverage --help',
                'usage: ./dev-cli.py coverage',
                'Run tests and show coverage.',
            ),
        )
