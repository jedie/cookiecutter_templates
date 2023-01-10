import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file
from manageprojects.git import Git
from manageprojects.test_utils.git_utils import init_git

from managetemplates.tests.base import BaseTestCase
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter
from managetemplates.utilities.test_project_utils import TestProject


class DjangoAppTemplateTestCase(BaseTestCase):
    def test_basic(self):
        pkg_path: Path = run_cookiecutter(
            template_name='django-app',
            final_name='your_cool_app',  # {{cookiecutter.package_name}} replaced!
            # force_recreate=True
            force_recreate=False,
        )
        test_project = TestProject(pkg_path)

        git_path = pkg_path / '.git'
        if not git_path.is_dir():
            # Newly generated -> git init
            git, git_hash = init_git(path=pkg_path)  # Helpful to display diffs, see below ;)
        else:
            # Reuse existing .git
            git = Git(cwd=git_path)

        output = test_project.check_output('poetry', 'check')
        self.assertEqual(output, 'All set!\n')

        if not Path(pkg_path / '.venv' / 'bin' / 'your_cool_app').is_file():
            output = test_project.check_output('make', 'install')
            self.assert_in('Poetry found, ok.', output)
            self.assert_in('Installing the current project: your_cool_app ', output)

        assert_is_file(pkg_path / '.venv' / 'bin' / 'pip')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'python')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'darker')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'flake8')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'coverage')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'twine')

        try:
            output = test_project.check_output('make', 'lint')
        except subprocess.CalledProcessError:
            # Just display what we should change in template to fix the code style:
            test_project.check_call('make', 'fix-code-style')
            self.display_git_diff(git)
            raise
        else:
            self.assert_in('poetry run darker --diff --check', output)
            self.assert_in('poetry run isort --check-only .', output)
            self.assert_in('poetry run flake8 .', output)

        output = test_project.check_output('make', 'test')
        self.assert_in('Ran 4 tests', output)
