import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file
from manageprojects.git import Git
from manageprojects.test_utils.git_utils import init_git

from managetemplates.tests.base import BaseTestCase
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter
from managetemplates.utilities.test_project_utils import TestProject


class PipenvPythonTemplateTestCase(BaseTestCase):
    def test_basic(self):
        pkg_path: Path = run_cookiecutter(
            template_name='pipenv-python',
            final_name='your_cool_package',  # {{cookiecutter.package_name}} replaced!
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

        output = test_project.check_output('make', 'fix-code-style')
        try:
            self.assert_in('.venv/bin/black ', output)
            self.assert_in('.venv/bin/isort .', output)
        except Exception:
            self.display_git_diff(git)
            raise

        subprocess.check_call(['make', 'lint'], cwd=pkg_path)

        output = test_project.check_output('make', 'test')
        self.assert_in('Ran 1 test', output)
