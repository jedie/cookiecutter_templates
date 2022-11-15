import os
import shlex
import subprocess
import sys
from pathlib import Path

import typer
from bx_py_utils.path import assert_is_dir, assert_is_file
from darker.__main__ import main as darker_main
from flake8.main.cli import main as flake8_main

import managetemplates
from managetemplates import __version__


PACKAGE_ROOT = Path(managetemplates.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT)
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')

app = typer.Typer()


def which(file_name: str) -> Path:
    venv_bin_path = Path(sys.executable).parent
    assert venv_bin_path.is_dir()
    bin_path = venv_bin_path / file_name
    if not bin_path.is_file():
        raise FileNotFoundError(f'File {file_name}!r not found in {venv_bin_path}')
    return bin_path


def verbose_check_call(*args, cwd=PACKAGE_ROOT):
    print(f'+{shlex.join(str(part) for part in args)}')
    subprocess.check_call(args, cwd=cwd)


def _call_darker(*, argv):
    # Work-a-round for:
    #
    #   File ".../site-packages/darker/linting.py", line 148, in _check_linter_output
    #     with Popen(  # nosec
    #   ...
    #   File "/usr/lib/python3.10/subprocess.py", line 1845, in _execute_child
    #     raise child_exception_type(errno_num, err_msg, err_filename)
    # FileNotFoundError: [Errno 2] No such file or directory: 'flake8'
    #
    # Just add .venv/bin/ to PATH:
    venv_path = PACKAGE_ROOT / '.venv' / 'bin'

    assert_is_dir(venv_path)
    assert_is_file(venv_path / 'flake8')
    venv_path = str(venv_path)
    if venv_path not in os.environ['PATH']:
        os.environ['PATH'] = venv_path + os.pathsep + os.environ['PATH']

    darker_main(argv=argv)


@app.command()
def fix_code_style():
    """
    Fix code style via darker
    """
    _call_darker(argv=['--color'])


@app.command()
def check_code_style(verbose: bool = True):
    _call_darker(argv=['--color', '--check'])
    if verbose:
        argv = ['--verbose']
    else:
        argv = []

    flake8_main(argv=argv)


@app.command()  # Just add this command to help page
def test():
    """
    Run unittests
    """
    # Use the CLI from unittest module and pass all args to it:
    verbose_check_call(sys.executable, '-m', 'unittest', *sys.argv[2:])


@app.command()
def coverage():
    """
    Run and show coverage.
    """
    coverage_bin = which('coverage')
    verbose_check_call(coverage_bin, 'run')
    verbose_check_call(coverage_bin, 'report', '--fail-under=30')
    verbose_check_call(coverage_bin, 'json')


def main():
    print(f'managetemplates v{__version__}')
    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        # Just use the CLI from unittest with all available options and origin --help output ;)
        return test()
    else:
        app()
