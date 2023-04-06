import logging
import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file

from managetemplates.tests.base import BaseTestCase, PackageTestMixin, TempGitRepo
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter
from managetemplates.utilities.test_project_utils import TestProject


class PoetryPythonTemplateTestCase(PackageTestMixin, BaseTestCase):
    template_name = 'poetry-python'
    pkg_name = 'your_cool_package'

    def test_basic(self):
        with self.assertLogs('cookiecutter', level=logging.DEBUG) as logs:
            pkg_path: Path = run_cookiecutter(
                template_name=self.template_name,
                force_recreate=True
                # force_recreate=False,
            )
        self.assert_in_content(
            got='\n'.join(logs.output),
            parts=(
                'poetry-python/cookiecutter.json',
                'Writing contents to file',

            ),
        )
        test_project = TestProject(pkg_path)

        with TempGitRepo(path=pkg_path, fresh=True) as temp_git:
            output = test_project.check_output('poetry', 'check')
            self.assertEqual(output, 'All set!\n')

            if not Path(pkg_path / '.venv' / 'bin' / 'your_cool_package').is_file():
                output = test_project.check_output('make', 'install')
                self.assert_in('Poetry found, ok.', output)
                self.assert_in('Installing the current project: your_cool_package (0.0.1)', output)

            assert_is_file(pkg_path / '.venv' / 'bin' / 'pip')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'python')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'your_cool_package')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'darker')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'flake8')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'coverage')
            assert_is_file(pkg_path / '.venv' / 'bin' / 'twine')

            output = test_project.check_output('make', 'fix-code-style', exit_on_error=True)

            self.assert_in('poetry run darker', output)
            self.assert_in('poetry run isort', output)

            subprocess.check_call(['make', 'lint'], cwd=pkg_path)

            # Run first "normal" tests, because tox has many more output and is slower ;)
            output = test_project.check_output('make', 'test')
            self.assert_in('python -m unittest', output)
            self.assert_in('Ran 6 tests in ', output)
            self.assert_in('OK', output)

            output = test_project.check_output('make', 'tox')
            self.assert_in('poetry run tox', output)
            self.assert_in('congratulations :)', output)

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
