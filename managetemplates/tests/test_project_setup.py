from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from bx_py_utils.test_utils.redirect import RedirectOut
from cli_base import run_pip_audit
from cli_base.cli_tools.code_style import assert_code_style
from cli_base.cli_tools.subprocess_utils import ToolsExecutor
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich, invoke
from cli_base.cli_tools.test_utils.subprocess_mocks import MockToolsExecutor
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from manageprojects.test_utils.subprocess import SimpleRunReturnCallback
from manageprojects.test_utils.subprocess import SubprocessCallMock as SubprocessCallMockOrigin
from packaging.version import Version

from managetemplates import __version__
from managetemplates.cli_app import main as cli_app_main
from managetemplates.cli_dev import PACKAGE_ROOT, packaging
from managetemplates.cli_dev import main as cli_dev_main
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
            rstrip_paths: list = [str(item) for item in rstrip_paths if item]  # e.g.: Path -> str

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

        with NoColorEnvRich():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'cli.py', args=['version'])
        self.assertIn(f'managetemplates v{__version__}', stdout)

        with NoColorEnvRich():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'dev-cli.py', args=['version'])
        self.assertIn(f'managetemplates v{__version__}', stdout)

    def test_code_style(self):
        return_code = assert_code_style(package_root=PACKAGE_ROOT)
        self.assertEqual(return_code, 0, 'Code style error, see output above!')

    def test_install(self):
        with (
            MockToolsExecutor(
                target=packaging,
                return_codes={'uv': 0, 'pip': 0},
                outputs={},
            ) as mock,
            RedirectOut() as buffer,
        ):
            cli_dev_main(args=('install',))

        self.assertEqual(
            mock.calls,
            [
                {'file_name': 'uv', 'popenargs': ('sync',)},
                {'file_name': 'pip', 'popenargs': ('install', '--no-deps', '-e', '.')},
            ],
        )
        self.assertEqual(buffer.stderr, '')
        self.assert_in_content(
            got=buffer.stdout,
            parts=('managetemplates v',),
        )

    def test_update(self):
        class NamedTemporaryFileMock:
            name = '/tmp/temp_requirements_MOCK.txt'

            def __init__(self, **kwargs):
                assert kwargs == {'prefix': 'requirements', 'suffix': '.txt'}, f'{kwargs=}'

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                assert exc_type is None, f'{exc_type=}'

        with (
            patch.object(tempfile, 'NamedTemporaryFile', NamedTemporaryFileMock),
            MockToolsExecutor(
                target=packaging,
                return_codes={'uv': 0, 'pre-commit': 0, 'pip': 0},
                outputs={},
            ) as mock1,
            MockToolsExecutor(
                target=run_pip_audit,
                return_codes={'pip-audit': 0, 'uv': 0},
                outputs={},
            ) as mock2,
            RedirectOut() as buffer,
        ):
            cli_dev_main(args=('update',))

        self.assertEqual(
            mock1.calls,
            [
                {'file_name': 'pip', 'popenargs': ('install', '-U', 'pip')},
                {'file_name': 'pip', 'popenargs': ('install', '-U', 'uv')},
                {'file_name': 'uv', 'popenargs': ('lock', '--upgrade')},
                {'file_name': 'uv', 'popenargs': ('sync',)},
                {'file_name': 'pre-commit', 'popenargs': ('autoupdate',)},
            ],
        )
        self.assertEqual(
            mock2.calls,
            [
                {
                    'file_name': 'uv',
                    'popenargs': (
                        'export',
                        '--no-header',
                        '--frozen',
                        '--no-editable',
                        '--no-emit-project',
                        '-o',
                        '/tmp/temp_requirements_MOCK.txt',
                    ),
                },
                {
                    'file_name': 'pip-audit',
                    'popenargs': (
                        '--strict',
                        '--require-hashes',
                        '--disable-pip',
                        '-r',
                        '/tmp/temp_requirements_MOCK.txt',
                    ),
                },
            ],
        )
        self.assertEqual(buffer.stderr, '')
        self.assert_in_content(
            got=buffer.stdout,
            parts=('managetemplates v',),
        )

    def test_update_template_req(self):
        with (
            patch('managetemplates.cli_app.print_version'),
            RedirectOut() as buffer,
            SubprocessCallMock(return_callback=SimpleRunReturnCallback(stdout='')) as call_mock,
        ):
            cli_app_main(args=('update-template-req',))

        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=RSTRIP_PATHS, with_cwd=True),
            [
                ['...$ .venv/bin/python3', '.../make-uv-python/update_requirements.py'],
                ['...$ .venv/bin/python3', '.../managed-django-project/update_requirements.py'],
                ['...$ .venv/bin/python3', '.../uv-python/update_requirements.py'],
                ['...$ .venv/bin/python3', '.../yunohost_django_package/update_requirements.py'],
            ],
        )
        self.assertEqual(buffer.stderr, '')
        self.assert_in_content(
            got=buffer.stdout,
            parts=(' Update requirements of ',),
        )

    def test_publish(self):
        with (
            patch.object(packaging, 'run_unittest_cli') as func1,
            patch.object(packaging, 'publish_package') as func2,
            RedirectOut() as buffer,
        ):
            cli_dev_main(args=('publish',))

        func1.assert_called_once()
        func2.assert_called_once()
        self.assertEqual(buffer.stderr, '')
        self.assert_in_content(
            got=buffer.stdout,
            parts=('managetemplates v',),
        )

    def test_filesystem_var_syntax(self):
        with RedirectOut() as buffer, self.assertRaises(SystemExit) as cm:
            cli_app_main(args=('fix-filesystem',))
        self.assertEqual(buffer.stderr, '')
        self.assert_in_content(
            got=buffer.stdout,
            parts=(
                'managetemplates v',
                'Nothing to rename, ok.',
            ),
        )
        self.assertEqual(cm.exception.code, 0)

    def test_file_content_var_syntax(self):
        stdout = invoke(cli_bin=PACKAGE_ROOT / 'cli.py', args=['fix-file-content'])
        self.assert_in_content(
            got=stdout,
            parts=('Nothing to fixed, ok.',),
        )

    def test_check_editor_config(self):
        check_editor_config(package_root=PACKAGE_ROOT)

        max_line_length = get_py_max_line_length(package_root=PACKAGE_ROOT)
        self.assertEqual(max_line_length, 119)

    def test_pre_commit_hooks(self):
        executor = ToolsExecutor(cwd=PACKAGE_ROOT)
        for command in ('migrate-config', 'validate-config', 'validate-manifest'):
            executor.verbose_check_call('pre-commit', command, exit_on_error=True)
