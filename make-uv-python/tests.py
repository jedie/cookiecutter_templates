import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.test_utils.assertion import assert_in

from managetemplates.tests.base import PackageTestBase, TempGitRepo


class MakeUvPythonTemplateTestCase(PackageTestBase):
    # force_recreate = True
    template_name = 'make-uv-python'
    pkg_name = 'your_cool_package'

    def test_basic(self):
        with TempGitRepo(path=self.pkg_path, fresh=True) as temp_git:

            if not Path(self.pkg_path / '.venv' / 'bin' / 'ruff').exists():
                output = self.test_project.check_output('make', 'install')
                assert_in(content=output, parts=('uv sync',))

            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'python')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'uv')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'nox')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'ruff')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'coverage')
            assert_is_file(self.pkg_path / '.venv' / 'bin' / 'twine')

            output = self.test_project.check_output('make', 'lint', exit_on_error=True)
            try:
                assert_in(content=output, parts=('ruff', 'All checks passed!'))
            except Exception:
                temp_git.display_git_diff()
                raise

            subprocess.check_call(['make', 'lint'], cwd=self.pkg_path)

            output = self.test_project.check_output('make', 'test')
            assert_in(content=output, parts=('Ran 4 test',))

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
