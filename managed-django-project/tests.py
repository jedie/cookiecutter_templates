from bx_py_utils.path import assert_is_file

from managetemplates.tests.base import PackageTestBase, TempGitRepo


class PiptoolsPythonTemplateTestCase(PackageTestBase):
    template_name = 'managed-django-project'
    pkg_name = 'your_cool_package'

    def test_basic(self):
        with TempGitRepo(path=self.pkg_path, fresh=True) as temp_git:

            manage_bin = self.pkg_path / 'manage.py'
            self.assert_is_executeable(manage_bin)

            ############################################################################
            # Bootstrap by call the ./manage.py

            output = self.test_project.check_output(manage_bin, 'version')
            self.assert_in('your_cool_package_project v0.0.1', output)

            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'python')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'tox')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip-compile')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip-sync')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'darker')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'flake8')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'coverage')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'twine')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'your_cool_package_project')

            output = self.test_project.check_output(manage_bin, '--help')
            self.assert_in('Available subcommands:', output)
            self.assert_in('[django]', output)
            self.assert_in('runserver', output)
            self.assert_in('[manage_django_project]', output)

            output = self.test_project.check_output(manage_bin, 'code_style')
            self.assert_in('Code style: OK', output)

            # TODO:
            # output = test_project.check_output(manage_bin, 'test')
            # self.assert_in('Ran 4 tests', output)

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
