from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich, invoke
from manageprojects.tests.base import BaseTestCase

from managetemplates import __version__, constants


class DevCliTestCase(BaseTestCase):

    def test_install(self):
        with NoColorEnvRich():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('install',))
        self.assert_in_content(
            got=output,
            parts=(
                'pip install --no-deps -e .',
                f'Successfully installed managetemplates-{__version__}',
            ),
        )

    def test_pass_nox_command(self):
        with NoColorEnvRich():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('nox', '--help'))
        self.assert_in_content(
            got=output,
            parts=(
                'usage: nox [-h] ',
                '--list-sessions',
            ),
        )
        with NoColorEnvRich():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('nox', '--list-sessions'))
        self.assert_in_content(
            got=output,
            parts=(
                '* tests-3.13',
                '* tests-3.12',
            ),
        )

    def test_pass_unittest_command(self):
        with NoColorEnvRich():
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
        with NoColorEnvRich():
            output = invoke(cli_bin=constants.PACKAGE_ROOT / 'dev-cli.py', args=('coverage', '--help'))
        self.assert_in_content(
            got=output,
            parts=(
                '.venv/bin/managetemplates_dev coverage --help',
                'usage: ./dev-cli.py coverage',
                'Run tests and show coverage.',
            ),
        )
