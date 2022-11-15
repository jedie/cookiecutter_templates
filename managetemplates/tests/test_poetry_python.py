import subprocess
from pathlib import Path
from unittest import TestCase

from bx_py_utils.path import assert_is_dir, assert_is_file
from manageprojects.git import Git
from manageprojects.test_utils.git_utils import init_git

from managetemplates.utilities.cookiecutter_utils import run_cookiecutter


class PoetryPythonTemplateTestCase(TestCase):
    def display_git_diff(self, git: Git):
        print('=' * 100)
        output = git.git_verbose_output('diff')
        print(output)
        print('=' * 100)

    def test_basic(self):
        pkg_path: Path = run_cookiecutter(
            template_name='poetry-python',
            final_name='your_cool_package',  # {{cookiecutter.package_name}} replaced!
            # force_recreate=True
            force_recreate=False,
        )
        assert_is_dir(pkg_path)

        git_path = pkg_path / '.git'
        if not git_path.exists():
            # Newly generated -> git init
            git, git_hash = init_git(path=pkg_path)  # Helpful to display diffs, see below ;)
        else:
            # Reuse existing .git
            git = Git(cwd=git_path)

        output = subprocess.check_output(['poetry', 'check'], cwd=pkg_path, text=True)
        self.assertEqual(output, 'All set!\n')

        output = subprocess.check_output(['make', 'install'], cwd=pkg_path, text=True)
        self.assertIn('Poetry found, ok.', output)
        self.assertIn('Installing the current project: your_cool_package (0.0.1)', output)

        assert_is_file(pkg_path / '.venv' / 'bin' / 'pip')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'python')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'your_cool_package')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'darker')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'flake8')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'coverage')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'twine')

        output = subprocess.check_output(['make', 'fix-code-style'], cwd=pkg_path, text=True)
        try:
            self.assertIn('poetry run black', output)
            self.assertIn('poetry run isort', output)
        except Exception:
            self.display_git_diff(git)
            raise

        subprocess.check_call(['make', 'lint'], cwd=pkg_path)

        # output = subprocess.check_output(['make', 'test'], cwd=pkg_path, text=True)
        # self.assertIn('TODO', output)
