import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file

from managetemplates.tests.base import PackageTestBase


class PoetryDjangoReuseableAppTemplateTestCase(PackageTestBase):
    template_name = 'poetry-django-app'
    pkg_name = 'your_reuseable_django_app'

    def test_basic(self):
        output = self.test_project.check_output('poetry', 'check')
        self.assertEqual(output, 'All set!\n')

        if not Path(self.pkg_path / '.venv' / 'bin' / 'your_cool_django_project').is_file():
            output = self.test_project.check_output('make', 'install')
            self.assert_in('Poetry found, ok.', output)
            self.assert_in('Installing the current project: your_reuseable_django_app (0.0.1)', output)

        assert_is_file(self.pkg_path / '.venv' / 'bin' / 'pip')
        assert_is_file(self.pkg_path / '.venv' / 'bin' / 'python')
        assert_is_file(self.pkg_path / '.venv' / 'bin' / 'django-admin')
        assert_is_file(self.pkg_path / '.venv' / 'bin' / 'darker')
        assert_is_file(self.pkg_path / '.venv' / 'bin' / 'flake8')
        assert_is_file(self.pkg_path / '.venv' / 'bin' / 'coverage')
        assert_is_file(self.pkg_path / '.venv' / 'bin' / 'twine')

        output = self.test_project.check_output('make', 'fix-code-style')

        self.assert_in('poetry run darker', output)
        self.assert_in('poetry run isort', output)

        subprocess.check_call(['make', 'lint'], cwd=self.pkg_path)

        # Run first "normal" tests, because tox has many more output and is slower ;)
        output = self.test_project.check_output('make', 'test')
        self.assert_in('./manage.sh test', output)
        self.assert_in('Ran 5 tests in ', output)
        self.assert_in('OK', output)

        output = self.test_project.check_output('make', 'tox')
        self.assert_in('poetry run tox', output)
        self.assert_in('coverage run', output)
        self.assert_in('congratulations :)', output)
