import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file

from managetemplates.tests.base import PackageTestBase, TempGitRepo


class MakeUvPythonTemplateTestCase(PackageTestBase):
    template_name = 'make-uv-python'
    pkg_name = 'your_cool_package'

    def test_basic(self):
        with TempGitRepo(path=self.pkg_path, fresh=True) as temp_git:

            if not Path(self.pkg_path / '.venv' / 'bin' / 'darker').exists():
                output = self.test_project.check_output('make', 'install')
                self.assert_in('.venv/bin/uv sync', output)

            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'python')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'uv')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'nox')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'darker')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'flake8')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'coverage')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'twine')

            output = self.test_project.check_output('make', 'fix-code-style', exit_on_error=True)
            try:
                self.assert_in('.venv/bin/darker', output)
                self.assert_in('.venv/bin/flake8 .', output)
            except Exception:
                temp_git.display_git_diff()
                raise

            subprocess.check_call(['make', 'lint'], cwd=self.pkg_path)

            output = self.test_project.check_output('make', 'test')
            self.assert_in('Ran 4 test', output)

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
