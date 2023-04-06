from bx_py_utils.path import assert_is_file

from managetemplates.tests.base import PackageTestBase, TempGitRepo


class PiptoolsPythonTemplateTestCase(PackageTestBase):
    template_name = 'piptools-python'
    pkg_name = 'your_cool_package'

    def test_basic(self):
        with TempGitRepo(path=self.pkg_path, fresh=True) as temp_git:

            cli_bin = self.pkg_path / 'cli.py'
            self.assert_is_executeable(cli_bin)

            ############################################################################
            # Bootstrap by call the ./cli.py

            output = self.test_project.check_output(cli_bin, 'version')
            self.assert_in('your_cool_package v0.0.1', output)

            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'python')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'tox')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip-compile')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip-sync')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'darker')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'flake8')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'coverage')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'twine')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'your_cool_package')

            output = self.test_project.check_output(cli_bin, '--help')
            self.assert_in('Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...', output)

            output = self.test_project.check_output(cli_bin, 'tox', '--help')
            self.assert_in('usage: tox [-h]', output)
            self.assert_in('list environments', output)
            self.assert_in('python -m tox --help', output)

            output = self.test_project.check_output(cli_bin, 'tox', 'list')
            self.assert_in('default environments:', output)
            self.assert_in('py311', output)
            self.assert_in('py310', output)
            self.assert_in('python -m tox list', output)

            output = self.test_project.check_output(cli_bin, 'check-code-style')
            self.assert_in('Code style: OK', output)

            output = self.test_project.check_output(cli_bin, 'test')
            self.assert_in('Ran 4 tests', output)

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
