import shutil
import sys
from pathlib import Path

import tomli
from bx_py_utils.path import assert_is_dir, assert_is_file
from bx_py_utils.test_utils.redirect import RedirectOut
from manageprojects.utilities.subprocess_utils import verbose_check_output

from managetemplates import __version__
from managetemplates.cli.cli_app import check_code_style, fix_code_style, install, publish, update
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
        with RedirectOut() as buffer:
            try:
                check_code_style(verbose=False)
            except SystemExit as err:
                if err.code == 0:
                    self.assertEqual(buffer.stderr, '')
                    self.assert_in_content(
                        got=buffer.stdout,
                        parts=(
                            '.venv/bin/darker',
                            '.venv/bin/flake8',
                            'Code style: OK',
                        ),
                    )
                    return  # Code style is ok -> Nothing to fix ;)
            else:
                raise AssertionError('No sys.exit() !')

        # Try to "auto" fix code style:

        with RedirectOut() as buffer:
            try:
                fix_code_style(verbose=False)
            except SystemExit as err:
                self.assertEqual(err.code, 0, 'Code style can not be fixed, see output above!')
            else:
                raise AssertionError('No sys.exit() !')

        self.assertEqual(buffer.stderr, '')
        self.assert_in_content(
            got=buffer.stdout,
            parts=(
                '.venv/bin/darker',
                'Code style fixed, OK.',
            ),
        )

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

        package_path = PACKAGE_ROOT / 'piptools-python' / '{{cookiecutter.package_name}}'
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
