from bx_py_utils.path import assert_is_file

from managetemplates.tests.base import PackageTestBase, TempGitRepo


class YunohostDjangoPackageTemplateTestCase(PackageTestBase):
    template_name = 'yunohost_django_package'
    pkg_name = 'django_example_ynh'

    def test_basic(self):
        with TempGitRepo(path=self.pkg_path, fresh=True, branch_name='master') as temp_git:
            makefile_path = self.pkg_path / 'Makefile'
            assert_is_file(makefile_path)

            poetry_lock = self.pkg_path / 'poetry.lock'
            req_txt = self.pkg_path / 'conf' / 'requirements.txt'
            if not (poetry_lock.is_file() and req_txt.is_file()):
                output = self.test_project.check_output('make', 'update')
                self.assert_in('poetry install', output)

            venv_path = self.pkg_path / '.venv'
            if not venv_path.is_dir():
                output = self.test_project.check_output('make', 'install')
                self.assert_in('poetry install', output)
                self.assert_in('Installing django-example', output)
                self.assert_in('Installing django-yunohost-integration', output)

            assert_is_file(venv_path / 'bin' / 'python')
            assert_is_file(venv_path / 'bin' / 'pip')
            assert_is_file(venv_path / 'bin' / 'django-admin')
            assert_is_file(venv_path / 'bin' / 'darker')
            assert_is_file(venv_path / 'bin' / 'black')

            self.test_project.check_call(
                'make',
                'pytest',
                extra_env=dict(
                    # The project used snapshot tests,
                    # because of very small differences,
                    # they do not match :(
                    RAISE_SNAPSHOT_ERRORS='false',  # Don't raise snapshot errors
                    GITHUB_ACTION='1',  # Don't try to check the github upstream version
                ),
            )

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
