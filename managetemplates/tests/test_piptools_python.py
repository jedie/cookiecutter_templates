import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file

from managetemplates.tests.base import BaseTestCase
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter
from managetemplates.utilities.test_project_utils import TestProject


class PiptoolsPythonTemplateTestCase(BaseTestCase):
    def test_basic(self):
        pkg_path: Path = run_cookiecutter(
            template_name='piptools-python',
            final_name='your_cool_package',  # {{cookiecutter.package_name}} replaced!
            # force_recreate=True
            force_recreate=False,
        )
        test_project = TestProject(pkg_path)

        cli_bin = pkg_path / 'cli.py'
        self.assert_is_executeable(cli_bin)

        ############################################################################
        # Bootstrap by call the ./cli.py

        output = test_project.check_output(cli_bin, 'version')
        self.assert_in('your_cool_package v0.0.1', output)

        assert_is_file(pkg_path / '.venv' / 'bin' / 'pip')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'python')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'pip-compile')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'pip-sync')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'darker')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'flake8')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'coverage')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'twine')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'your_cool_package')

        output = test_project.check_output(cli_bin, '--help')
        self.assert_in('Usage: your_cool_package [OPTIONS] COMMAND [ARGS]...', output)

        try:
            output = test_project.check_output(cli_bin, 'check-code-style')
        except subprocess.CalledProcessError:
            # Just display what we should change in template to fix the code style:
            test_project.check_call(
                'black', '--skip-string-normalization', '--line-length', '119', '--diff', '.'
            )
            raise
        else:
            self.assert_in('darker exit code: 0', output)
            self.assert_in('flake8 exit code: 0', output)

        output = test_project.check_output(cli_bin, 'test')
        self.assert_in('Ran 2 tests', output)
