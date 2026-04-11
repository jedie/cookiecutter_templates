from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.test_utils.assertion import assert_in

from managetemplates.tests.base import PackageTestBase, TempGitRepo


class UvPythonTemplateTestCase(PackageTestBase):
    # force_recreate = True
    template_name = 'uv-python'
    pkg_name = 'your_cool_package'

    def test_basic(self):
        with TempGitRepo(path=self.pkg_path, fresh=True) as temp_git:

            ############################################################################
            # Bootstrap by call the ./cli.py

            cli_bin = self.pkg_path / 'cli.py'
            self.assert_is_executeable(cli_bin)

            output = self.test_project.check_output(cli_bin, 'version')
            assert_in(content=output, parts=('your-cool-package v0.0.1',))

            assert_is_file(self.pkg_path / '.venv-app' / 'bin' / 'pip')
            assert_is_file(self.pkg_path / '.venv-app' / 'bin' / 'python')
            assert_is_file(self.pkg_path / '.venv-app' / 'bin' / 'your_cool_package')

            output = self.test_project.check_output(cli_bin, '--help')
            assert_in(content=output, parts=('usage: your-cool-package [-h]',))

            ############################################################################
            # Bootstrap by call the ./dev-cli.py

            dev_cli_bin = self.pkg_path / 'dev-cli.py'
            self.assert_is_executeable(dev_cli_bin)

            output = self.test_project.check_output(dev_cli_bin, 'version')
            assert_in(content=output, parts=('your_cool_package v0.0.1',))

            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'python')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'nox')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'uv')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'ruff')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'coverage')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'twine')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'your_cool_package')  # The normal CLI

            output = self.test_project.check_output(dev_cli_bin, '--help')
            assert_in(
                content=output,
                parts=(
                    'usage: ./dev-cli.py [-h]',
                    ' lint ',
                    ' coverage ',
                    ' publish ',
                    ' update-readme-history ',
                ),
            )

            output = self.test_project.check_output(dev_cli_bin, 'nox', '--help')
            assert_in(
                content=output,
                parts=(
                    'usage: nox [-h]',
                    'List all available sessions',
                    '.venv/bin/nox --help',
                ),
            )

            output = self.test_project.check_output(dev_cli_bin, 'nox', '-l')
            assert_in(
                content=output,
                parts=(
                    'tests-3.13',
                    'tests-3.12',
                    '.venv/bin/nox -l',
                ),
            )

            output = self.test_project.check_output(dev_cli_bin, 'lint')
            try:
                assert_in(content=output, parts=('ruff', 'All checks passed!'))
            except Exception:
                temp_git.display_git_diff()
                raise

            output = self.test_project.check_output(
                dev_cli_bin,
                'test',
                extra_env=dict(
                    GITHUB_ACTION='1',  # Disable README history test ;)
                ),
            )
            assert_in(content=output, parts=('Ran 8 tests',))

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
