import sys
from pathlib import Path
from unittest import TestCase

import tomli
from bx_py_utils.path import assert_is_file

from managetemplates import __version__
from managetemplates.cli.cli_app import (
    check_code_style,
    fix_code_style,
    install,
    publish,
    update,
    version,
)
from managetemplates.constants import PACKAGE_ROOT
from managetemplates.utilities.test_project_utils import Call, SubprocessCallMock


VENV_BIN_PATH = Path(sys.executable).parent


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        assert_is_file(pyproject_toml_path)

        self.assertIsNotNone(__version__)

        pyproject_toml = tomli.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['project']['version']

        self.assertEqual(__version__, pyproject_version)

        self.assertEqual(version(), f'{{ cookiecutter.package_name }} v{__version__}')

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
        with SubprocessCallMock() as call_mock:
            install()

        self.assertEqual(
            call_mock.calls,
            [
                Call(
                    args=(
                        [
                            VENV_BIN_PATH / 'pip-sync',
                            PACKAGE_ROOT / 'managetemplates/requirements.txt',
                        ],
                    ),
                    kwargs={},
                ),
                Call(
                    args=([VENV_BIN_PATH / 'pip', 'install', '-e', '.'],),
                    kwargs={},
                ),
            ],
        )

    def test_update(self):
        with SubprocessCallMock() as call_mock:
            update()

        self.assertEqual(
            call_mock.calls,
            [
                Call(
                    args=(
                        [
                            VENV_BIN_PATH / 'pip-compile',
                            '--verbose',
                            '--upgrade',
                            '--allow-unsafe',
                            '--generate-hashes',
                            PACKAGE_ROOT / 'managetemplates/requirements.in',
                            '--output-file',
                            PACKAGE_ROOT / 'managetemplates/requirements.txt',
                        ],
                    ),
                    kwargs={},
                )
            ],
        )

    def test_publish(self):
        with SubprocessCallMock() as call_mock:
            publish()

        self.assertEqual(
            call_mock.calls,
            [
                Call(args=([VENV_BIN_PATH / 'python', '-m', 'unittest'],), kwargs={}),
                Call(args=([VENV_BIN_PATH / 'python', '-m', 'build'],), kwargs={}),
                Call(args=([VENV_BIN_PATH / 'twine', 'check', 'dist/*'],), kwargs={}),
                Call(args=([VENV_BIN_PATH / 'twine', 'upload', 'dist/*'],), kwargs={}),
                Call(
                    args=(
                        [
                            Path('/usr/bin/git'),
                            'tag',
                            '-a',
                            f'v{__version__}',
                            '-m',
                            f'publish version v{__version__}',
                        ],
                    ),
                    kwargs={'cwd': PACKAGE_ROOT},
                ),
                Call(
                    args=([Path('/usr/bin/git'), 'push', '--tags'],), kwargs={'cwd': PACKAGE_ROOT}
                ),
            ],
        )
