import shutil
import subprocess
import sys
from pathlib import Path

import tomli
from bx_py_utils.path import assert_is_dir, assert_is_file
from manageprojects.test_utils.click_cli_utils import subprocess_cli
from manageprojects.utilities import code_style
from manageprojects.utilities.subprocess_utils import verbose_check_output

from managetemplates import __version__
from managetemplates.cli.cli_app import fix_file_content, fix_filesystem, install, publish, update
from managetemplates.constants import PACKAGE_ROOT, REQ_DEV_TXT_PATH, REQ_TXT_PATH
from managetemplates.tests.base import BaseTestCase
from managetemplates.utilities.test_project_utils import Call, SubprocessCallMock


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
        with SubprocessCallMock(without_kwargs=True) as call_mock:
            install()

        self.assertEqual(
            call_mock.calls,
            [
                Call(
                    args=(
                        [
                            str(VENV_BIN_PATH / 'pip-sync'),
                            str(PACKAGE_ROOT / 'managetemplates/requirements.dev.txt'),
                        ],
                    ),
                    kwargs=None,
                ),
                Call(args=([str(VENV_BIN_PATH / 'pip'), 'install', '-e', '.'],), kwargs=None),
            ],
        )

    def test_update(self):
        with SubprocessCallMock(without_kwargs=True) as call_mock:
            update()

        package_path = PACKAGE_ROOT / 'piptools-python' / '{{ cookiecutter.package_name }}'
        assert_is_dir(package_path)

        req_prod_txt_path = package_path / 'requirements.txt'
        assert_is_file(req_prod_txt_path)

        req_dev_txt_path = package_path / 'requirements.dev.txt'
        assert_is_file(req_dev_txt_path)

        self.assertEqual(
            call_mock.calls,
            [
                Call(
                    args=(
                        [
                            str(VENV_BIN_PATH / 'pip-compile'),
                            '--verbose',
                            '--allow-unsafe',
                            '--resolver=backtracking',
                            '--upgrade',
                            '--generate-hashes',
                            'pyproject.toml',
                            '--output-file',
                            str(REQ_TXT_PATH),
                        ],
                    ),
                    kwargs=None,
                ),
                Call(
                    args=(
                        [
                            str(VENV_BIN_PATH / 'pip-compile'),
                            '--verbose',
                            '--allow-unsafe',
                            '--resolver=backtracking',
                            '--upgrade',
                            '--generate-hashes',
                            'pyproject.toml',
                            '--extra=tests',
                            '--output-file',
                            str(REQ_DEV_TXT_PATH),
                        ],
                    ),
                    kwargs=None,
                ),
                Call(
                    args=(
                        [
                            str(VENV_BIN_PATH / 'pip-compile'),
                            '--verbose',
                            '--allow-unsafe',
                            '--resolver=backtracking',
                            '--upgrade',
                            '--generate-hashes',
                            'pyproject.toml',
                            '--output-file',
                            str(req_prod_txt_path),
                        ],
                    ),
                    kwargs=None,
                ),
                Call(
                    args=(
                        [
                            str(VENV_BIN_PATH / 'pip-compile'),
                            '--verbose',
                            '--allow-unsafe',
                            '--resolver=backtracking',
                            '--upgrade',
                            '--generate-hashes',
                            'pyproject.toml',
                            '--extra=tests',
                            '--output-file',
                            str(req_dev_txt_path),
                        ],
                    ),
                    kwargs=None,
                ),
            ],
        )

    def test_publish(self):
        origin_sys_argv = sys.argv[:]
        try:
            sys.argv = ['./cli.py', 'publish']
            with SubprocessCallMock(without_kwargs=True) as call_mock:
                publish()
        finally:
            sys.argv = origin_sys_argv

        git_bin = shutil.which('git')
        self.assertEqual(
            call_mock.calls,
            [
                Call(
                    args=([sys.executable, '-m', 'unittest', '--verbose', '--locals', '--buffer'],),
                    kwargs=None,
                ),
                Call(args=([sys.executable, '-m', 'build'],), kwargs=None),
                Call(args=([str(VENV_BIN_PATH / 'twine'), 'check', 'dist/*'],), kwargs=None),
                Call(args=([str(VENV_BIN_PATH / 'twine'), 'upload', 'dist/*'],), kwargs=None),
                Call(
                    args=(
                        [
                            git_bin,
                            'tag',
                            '-a',
                            f'v{__version__}',
                            '-m',
                            f'publish version v{__version__}',
                        ],
                    ),
                    kwargs=None,
                ),
                Call(args=([git_bin, 'push', '--tags'],), kwargs=None),
            ],
        )

    def test_filesystem_var_syntax(self):
        try:
            fix_filesystem()
        except SystemExit as err:
            self.assertEqual(err.code, 0)

    def test_file_content_var_syntax(self):
        try:
            fix_file_content()
        except SystemExit as err:
            self.assertEqual(err.code, 0)
