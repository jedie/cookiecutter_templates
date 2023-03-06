import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import tomli
from bx_py_utils.path import assert_is_dir, assert_is_file
from manageprojects.test_utils.click_cli_utils import invoke_click, subprocess_cli
from manageprojects.test_utils.subprocess import SubprocessCallMock
from manageprojects.utilities import code_style
from manageprojects.utilities.subprocess_utils import verbose_check_output

import managetemplates
from managetemplates import __version__
from managetemplates.cli import cli_app
from managetemplates.cli.cli_app import cli
from managetemplates.constants import PACKAGE_ROOT
from managetemplates.tests.base import BaseTestCase


VENV_BIN_PATH = Path(sys.executable).parent


class ProjectSetupTestCase(BaseTestCase):
    def test_version(self):
        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        assert_is_file(pyproject_toml_path)

        self.assertIsNotNone(__version__)

        pyproject_toml = tomli.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['project']['version']

        self.assertEqual(__version__, pyproject_version)

        output = verbose_check_output(PACKAGE_ROOT / 'cli.py', 'version')
        self.assert_in(f'managetemplates v{__version__}', output)

    def test_code_style(self):
        cli_bin = PACKAGE_ROOT / 'cli.py'
        assert_is_file(cli_bin)

        try:
            output = subprocess_cli(
                cli_bin=cli_bin,
                args=('check-code-style',),
                exit_on_error=False,
            )
        except subprocess.CalledProcessError as err:
            self.assert_in_content(  # darker was called?
                got=err.stdout,
                parts=('.venv/bin/darker',),
            )
        else:
            if 'Code style: OK' in output:
                self.assert_in_content(  # darker was called?
                    got=output,
                    parts=('.venv/bin/darker',),
                )
                return  # Nothing to fix -> OK

        # Try to "auto" fix code style:

        try:
            output = subprocess_cli(
                cli_bin=cli_bin,
                args=('fix-code-style',),
                exit_on_error=False,
            )
        except subprocess.CalledProcessError as err:
            output = err.stdout

        self.assert_in_content(  # darker was called?
            got=output,
            parts=('.venv/bin/darker',),
        )

        # Check again and display the output:

        try:
            code_style.check(package_root=PACKAGE_ROOT)
        except SystemExit as err:
            self.assertEqual(err.code, 0, 'Code style error, see output above!')

    def test_install(self):
        with SubprocessCallMock() as call_mock:
            stdout = invoke_click(cli, 'install')

        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=(PACKAGE_ROOT,)),
            [
                ['.../.venv/bin/pip-sync', '.../managetemplates/requirements.dev.txt'],
                ['.../.venv/bin/pip', 'install', '-e', '.'],
            ],
        )
        self.assert_in_content(
            got=stdout,
            parts=('pip install -e .',),
        )

    def test_update(self):
        with SubprocessCallMock() as call_mock:
            invoke_click(cli, 'update')

        package_path = PACKAGE_ROOT / 'piptools-python' / '{{ cookiecutter.package_name }}'
        assert_is_dir(package_path)

        req_prod_txt_path = package_path / 'requirements.txt'
        assert_is_file(req_prod_txt_path)

        req_dev_txt_path = package_path / 'requirements.dev.txt'
        assert_is_file(req_dev_txt_path)

        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=(PACKAGE_ROOT,)),
            [
                ['.../.venv/bin/pip', 'install', '-U', 'pip'],
                ['.../.venv/bin/pip', 'install', '-U', 'pip-tools'],
                [
                    '.../.venv/bin/pip-compile',
                    '--verbose',
                    '--allow-unsafe',
                    '--resolver=backtracking',
                    '--upgrade',
                    '--generate-hashes',
                    'pyproject.toml',
                    '--output-file',
                    '.../managetemplates/requirements.txt',
                ],
                [
                    '.../.venv/bin/pip-compile',
                    '--verbose',
                    '--allow-unsafe',
                    '--resolver=backtracking',
                    '--upgrade',
                    '--generate-hashes',
                    'pyproject.toml',
                    '--extra=tests',
                    '--output-file',
                    '.../managetemplates/requirements.dev.txt',
                ],
                [
                    '.../.venv/bin/pip-compile',
                    '--verbose',
                    '--allow-unsafe',
                    '--resolver=backtracking',
                    '--upgrade',
                    '--generate-hashes',
                    'pyproject.toml',
                    '--output-file',
                    '.../piptools-python/{{ cookiecutter.package_name }}/requirements.txt',
                ],
                [
                    '.../.venv/bin/pip-compile',
                    '--verbose',
                    '--allow-unsafe',
                    '--resolver=backtracking',
                    '--upgrade',
                    '--generate-hashes',
                    'pyproject.toml',
                    '--extra=tests',
                    '--output-file',
                    '.../piptools-python/{{ cookiecutter.package_name }}/requirements.dev.txt',
                ],
            ],
        )

    def test_publish(self):
        with patch.object(cli_app, '_run_unittest_cli') as func1, patch.object(cli_app, 'publish_package') as func2:
            stdout = invoke_click(cli, 'publish')

        func1.assert_called_once_with(verbose=False, exit_after_run=False)
        func2.assert_called_once_with(module=managetemplates, package_path=PACKAGE_ROOT)
        self.assertEqual(stdout, '')

    def test_filesystem_var_syntax(self):
        stdout = invoke_click(cli, 'fix-filesystem')
        self.assert_in_content(
            got=stdout,
            parts=('Nothing to rename, ok.',),
        )

    def test_file_content_var_syntax(self):
        stdout = invoke_click(cli, 'fix-file-content')
        self.assert_in_content(
            got=stdout,
            parts=('Nothing to fixed, ok.',),
        )
