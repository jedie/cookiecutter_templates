from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.test_utils.assertion import assert_in

from managetemplates.tests.base import PackageTestBase, TempGitRepo


class ManageDjangoProjectTemplateTestCase(PackageTestBase):
    # force_recreate = True
    template_name = 'managed-django-project'
    pkg_name = 'your_cool_package'

    def test_basic(self):
        with TempGitRepo(path=self.pkg_path, fresh=True) as temp_git:

            manage_bin = self.pkg_path / 'manage.py'
            self.assert_is_executeable(manage_bin)

            ############################################################################
            # Bootstrap by call the ./manage.py

            output = self.test_project.check_output(manage_bin, 'version')
            assert_in(content=output, parts=('your_cool_package_project v0.0.1',))

            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'python')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'nox')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'uv')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'ruff')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'coverage')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'twine')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'your_cool_package_project')

            output = self.test_project.check_output(manage_bin, '--help')
            assert_in(
                content=output,
                parts=(
                    'Available subcommands:',
                    '[django]',
                    'runserver',
                    '[manage_django_project]',
                ),
            )

            output = self.test_project.check_output(manage_bin, 'code_style')
            try:
                assert_in(content=output, parts=('ruff', 'All checks passed!'))
            except Exception:
                temp_git.display_git_diff()
                raise

            output = self.test_project.check_output(manage_bin, 'test')
            assert_in(content=output, parts=('Ran 12 tests',))

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
