import logging
import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file

from managetemplates.tests.base import BaseTestCase, PackageTestMixin, TempGitRepo
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter
from managetemplates.utilities.test_project_utils import TestProject


class PipenvPythonTemplateTestCase(PackageTestMixin, BaseTestCase):
    template_name = 'pipenv-python'
    pkg_name = 'your_cool_package'

    def test_basic(self):
        with self.assertLogs('cookiecutter', level=logging.DEBUG) as logs:
            pkg_path: Path = run_cookiecutter(
                template_name=self.template_name,
                # force_recreate=True
                force_recreate=False,
            )
        self.assert_in_content(
            got='\n'.join(logs.output),
            parts=(
                'pipenv-python/cookiecutter.json',
                'Writing contents to file',

            ),
        )
        test_project = TestProject(
            pkg_path,
            base_extra_env=dict(PIPENV_IGNORE_VIRTUALENVS='1'),
        )

        with TempGitRepo(path=pkg_path, fresh=True) as temp_git:

            if not Path(pkg_path / '.venv' / 'bin' / 'darker').exists():
                output = test_project.check_output('make', 'install')
                self.assert_in('Installing dependencies from Pipfile.lock', output)

            assert_is_file(pkg_path / '.venv' / 'bin' / 'pip')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'python')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'pipenv')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'darker')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'flake8')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'coverage')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'twine')

            output = test_project.check_output('make', 'fix-code-style', exit_on_error=True)
            try:
                self.assert_in('pipenv run darker', output)
            except Exception:
                temp_git.display_git_diff()
                raise

            subprocess.check_call(['make', 'lint'], cwd=pkg_path)

            output = test_project.check_output('make', 'test')
            self.assert_in('Ran 3 test', output)

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
