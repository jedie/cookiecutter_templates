import shutil
import sys
from pathlib import Path

import tomli
from bx_py_utils.path import assert_is_file
from manageprojects.utilities.subprocess_utils import verbose_check_output

from managetemplates import __version__
from managetemplates.cli.cli_app import check_code_style, fix_code_style, install, publish, update
from managetemplates.constants import PACKAGE_ROOT
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
        self.assert_in(f'\nmanagetemplates v{__version__}\n', output)

    def test_code_style(self):
        try:
            fix_code_style()
        except SystemExit as err:
            self.assertEqual(err.code, 0)
        else:
            raise AssertionError('No sys.exit() !')

        try:
            check_code_style(verbose=False)
        except SystemExit as err:
            self.assertEqual(err.code, 0)
        else:
            raise AssertionError('No sys.exit() !')

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
                            str(PACKAGE_ROOT / 'managetemplates/requirements.txt'),
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

        self.assertEqual(
            call_mock.calls,
            [
                Call(
                    args=(
                        [
                            str(VENV_BIN_PATH / 'pip-compile'),
                            '--verbose',
                            '--upgrade',
                            '--allow-unsafe',
                            '--generate-hashes',
                            str(PACKAGE_ROOT / 'managetemplates/requirements.in'),
                            '--output-file',
                            str(PACKAGE_ROOT / 'managetemplates/requirements.txt'),
                        ],
                    ),
                    kwargs=None,
                )
            ],
        )

    def test_publish(self):
        with SubprocessCallMock(without_kwargs=True) as call_mock:
            publish()

        git_bin = shutil.which('git')
        self.assertEqual(
            call_mock.calls,
            [
                Call(args=([str(VENV_BIN_PATH / 'python'), '-m', 'unittest'],), kwargs=None),
                Call(args=([str(VENV_BIN_PATH / 'python'), '-m', 'build'],), kwargs=None),
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
