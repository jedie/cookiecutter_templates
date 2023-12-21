import subprocess
from pathlib import Path
from unittest.mock import patch

from bx_py_utils.path import assert_is_dir, assert_is_file
from cli_base.cli_tools.code_style import assert_code_style
from manageprojects.test_utils.click_cli_utils import invoke_click
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from manageprojects.test_utils.subprocess import SubprocessCallMock as SubprocessCallMockOrigin
from packaging.version import Version

from managetemplates import __version__
from managetemplates.cli.cli_app import cli
from managetemplates.cli.dev import PACKAGE_ROOT
from managetemplates.cli.dev import cli as dev_cli
from managetemplates.constants import PY_BIN_PATH
from managetemplates.tests.base import BaseTestCase


RSTRIP_PATHS = (PY_BIN_PATH.parent, PACKAGE_ROOT)


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

        cli_bin = PACKAGE_ROOT / 'cli.py'
        assert_is_file(cli_bin)

        output = subprocess.check_output([cli_bin, 'version'], text=True)
        self.assertIn(f'managetemplates v{__version__}', output)

        dev_cli_bin = PACKAGE_ROOT / 'dev-cli.py'
        assert_is_file(dev_cli_bin)

        output = subprocess.check_output([dev_cli_bin, 'version'], text=True)
        self.assertIn(f'managetemplates v{__version__}', output)

    def test_code_style(self):
        return_code = assert_code_style(package_root=PACKAGE_ROOT)
        self.assertEqual(return_code, 0, 'Code style error, see output above!')

    def test_install(self):
        with SubprocessCallMock() as call_mock:
            stdout = invoke_click(dev_cli, 'install')

        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=RSTRIP_PATHS),
            [
                ['.../bin/pip-sync', '.../requirements.dev.txt'],
                ['.../bin/pip', 'install', '--no-deps', '-e', '.'],
            ],
        )
        self.assert_in_content(
            got=stdout,
            parts=('pip install --no-deps -e .',),
        )

    def test_update(self):
        with SubprocessCallMock() as call_mock:
            invoke_click(dev_cli, 'update')

        package_path = PACKAGE_ROOT / 'piptools-python' / '{{ cookiecutter.package_name }}'
        assert_is_dir(package_path)

        req_prod_txt_path = package_path / 'requirements.txt'
        assert_is_file(req_prod_txt_path)

        req_dev_txt_path = package_path / 'requirements.dev.txt'
        assert_is_file(req_dev_txt_path)

        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=RSTRIP_PATHS),
            [
                ['.../bin/pip', 'install', '-U', 'pip'],
                ['.../bin/pip', 'install', '-U', 'pip-tools'],
                [
                    '.../bin/pip-compile',
                    '--verbose',
                    '--allow-unsafe',
                    '--resolver=backtracking',
                    '--upgrade',
                    '--generate-hashes',
                    'pyproject.toml',
                    '--output-file',
                    'requirements.txt',
                ],
                [
                    '.../bin/pip-compile',
                    '--verbose',
                    '--allow-unsafe',
                    '--resolver=backtracking',
                    '--upgrade',
                    '--generate-hashes',
                    'pyproject.toml',
                    '--extra=dev',
                    '--output-file',
                    'requirements.dev.txt',
                ],
                ['.../bin/safety', 'check', '-r', 'requirements.dev.txt'],
                ['.../bin/pip-sync', 'requirements.dev.txt'],
            ],
        )

    def test_update_template_req(self):
        with SubprocessCallMock() as call_mock:
            invoke_click(cli, 'update-template-req')

        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=RSTRIP_PATHS, with_cwd=True),
            [
                ['.../managed-django-project$ .../bin/python', 'update_requirements.py'],
                ['.../pipenv-python$ .../bin/python', 'update_requirements.py'],
                ['.../piptools-python$ .../bin/python', 'update_requirements.py'],
                ['.../poetry-django-app$ .../bin/python', 'update_requirements.py'],
                ['.../poetry-python$ .../bin/python', 'update_requirements.py'],
                ['.../yunohost_django_package$ .../bin/python', 'update_requirements.py'],
            ],
        )

    def test_publish(self):
        with (
            patch('managetemplates.cli.dev.run_unittest_cli') as func1,
            patch('managetemplates.cli.dev.publish_package') as func2,
        ):
            stdout = invoke_click(dev_cli, 'publish')

        func1.assert_called_once()
        func2.assert_called_once()
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
