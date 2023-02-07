import logging
import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file
from manageprojects.git import Git
from manageprojects.test_utils.git_utils import init_git

from managetemplates.tests.base import BaseTestCase
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter
from managetemplates.utilities.test_project_utils import TestProject


class PoetryDjangoReuseableAppTemplateTestCase(BaseTestCase):
    def test_basic(self):
        with self.assertLogs('cookiecutter', level=logging.DEBUG) as logs:
            pkg_path: Path = run_cookiecutter(
                template_name='poetry-django-app',
                final_name='your_reuseable_django_app',  # {{ cookiecutter.package_name }} replaced!
                # force_recreate=True
                force_recreate=False,
            )
        logs = '\n'.join(logs.output)
        self.assert_in_content(
            got=logs,
            parts=(
                'poetry-django-app/cookiecutter.json',
                'Writing contents to file',
                '/.tests/poetry-django-app/your_reuseable_django_app/',
            ),
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

        if not Path(pkg_path / '.venv' / 'bin' / 'your_cool_django_project').is_file():
            output = test_project.check_output('make', 'install')
            self.assert_in('Poetry found, ok.', output)
            self.assert_in('Installing the current project: your_reuseable_django_app (0.0.1)', output)

        assert_is_file(pkg_path / '.venv' / 'bin' / 'pip')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'python')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'django-admin')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'darker')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'flake8')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'coverage')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'twine')

        output = test_project.check_output('make', 'fix-code-style')
        try:
            self.assert_in('poetry run darker', output)
            self.assert_in('poetry run black', output)
            self.assert_in('poetry run isort', output)
        except Exception:
            self.display_git_diff(git)
            raise

        subprocess.check_call(['make', 'lint'], cwd=pkg_path)

        output = test_project.check_output('make', 'tox')
        self.assert_in('poetry install', output)
        self.assert_in('make test', output)
        self.assert_in('Ran 4 tests', output)
