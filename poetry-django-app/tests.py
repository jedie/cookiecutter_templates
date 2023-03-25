import logging
import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file

from managetemplates.tests.base import BaseTestCase, PackageTestMixin
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter
from managetemplates.utilities.test_project_utils import TestProject


class PoetryDjangoReuseableAppTemplateTestCase(PackageTestMixin, BaseTestCase):
    template_name = 'poetry-django-app'
    pkg_name = 'your_reuseable_django_app'

    def test_basic(self):
        with self.assertLogs('cookiecutter', level=logging.DEBUG) as logs:
            pkg_path: Path = run_cookiecutter(
                template_name=self.template_name,
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

        self.assert_in('poetry run darker', output)
        self.assert_in('poetry run isort', output)

        subprocess.check_call(['make', 'lint'], cwd=pkg_path)

        # Run first "normal" tests, because tox has many more output and is slower ;)
        output = test_project.check_output('make', 'test')
        self.assert_in('./manage.sh test', output)
        self.assert_in('Ran 5 tests in ', output)
        self.assert_in('OK', output)

        output = test_project.check_output('make', 'tox')
        self.assert_in('poetry run tox', output)
        self.assert_in('coverage run', output)
        self.assert_in('congratulations :)', output)
