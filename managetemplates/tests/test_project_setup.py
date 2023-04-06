import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from bx_py_utils.path import assert_is_dir, assert_is_file
from manageprojects.test_utils.click_cli_utils import invoke_click, subprocess_cli
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from manageprojects.test_utils.subprocess import SubprocessCallMock as SubprocessCallMockOrigin
from manageprojects.utilities import code_style
from manageprojects.utilities.subprocess_utils import verbose_check_output
from packaging.version import Version

import managetemplates
from managetemplates import __version__
from managetemplates.cli import cli_app
from managetemplates.cli.cli_app import cli
from managetemplates.constants import PACKAGE_ROOT
from managetemplates.tests.base import BaseTestCase


VENV_BIN_PATH = Path(sys.executable).parent


class SubprocessCallMock(SubprocessCallMockOrigin):
    # TODO: Move back to manageprojects!
    def rstrip_paths(self, path, rstrip_paths):
        if rstrip_paths:
            if isinstance(path, Path):
                path = str(path)
            for rstrip_path in rstrip_paths:
                if path.startswith(rstrip_path):
                    path = f'...{path.removeprefix(rstrip_path)}'
        return path

    def get_popenargs(self, rstrip_paths: tuple | None = None, with_cwd: bool = False) -> list:
        if rstrip_paths:
            rstrip_paths = [str(item) for item in rstrip_paths if item]  # e.g.: Path -> str

        result = []
        for call in self.calls:
            if rstrip_paths:
                temp = []

                if with_cwd and (cwd := call.kwargs.get('cwd')):
                    prog = call.popenargs[0]

                    try:
                        prog = Path(prog).absolute()
                        prog = prog.relative_to(Path(cwd).absolute())
                    except ValueError as err:
                        print(err)
                        # e.g.: {arg} is not in the subpath of {cwd}
                        pass

                    prog = self.rstrip_paths(prog, rstrip_paths)
                    cwd = self.rstrip_paths(cwd, rstrip_paths)
                    arg = f'{cwd}$ {prog}'
                    call.popenargs[0] = arg

                for arg in call.popenargs:
                    arg = self.rstrip_paths(arg, rstrip_paths)
                    temp.append(arg)

                result.append(temp)

            else:
                result.append(call.popenargs)

        return result


class ProjectSetupTestCase(BaseTestCase):
    def test_version(self):
        self.assertIsNotNone(__version__)

        version = Version(__version__)  # Will raise InvalidVersion() if wrong formatted
        self.assertEqual(str(version), __version__)

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
                ['.../.venv/bin/pip', 'install', '--no-deps', '-e', '.'],
            ],
        )
        self.assert_in_content(
            got=stdout,
            parts=('pip install --no-deps -e .',),
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
                    '--allow-unsafe',
                    '--resolver=backtracking',
                    '--upgrade',
                    '--generate-hashes',
                    'pyproject.toml',
                    '--extra=tests',
                    '--output-file',
                    '.../managetemplates/requirements.dev.txt',
                ],
            ],
        )

    def test_update_template_req(self):
        with SubprocessCallMock() as call_mock:
            invoke_click(cli, 'update-template-req')

        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=(PACKAGE_ROOT,), with_cwd=True),
            [
                ['.../managed-django-project$ .../.venv/bin/python', 'update_requirements.py'],
                ['.../pipenv-python$ .../.venv/bin/python', 'update_requirements.py'],
                ['.../piptools-python$ .../.venv/bin/python', 'update_requirements.py'],
                ['.../poetry-django-app$ .../.venv/bin/python', 'update_requirements.py'],
                ['.../poetry-python$ .../.venv/bin/python', 'update_requirements.py'],
                ['.../yunohost_django_package$ .../.venv/bin/python', 'update_requirements.py'],
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

    def test_check_editor_config(self):
        check_editor_config(package_root=PACKAGE_ROOT)

        max_line_length = get_py_max_line_length(package_root=PACKAGE_ROOT)
        self.assertEqual(max_line_length, 119)
