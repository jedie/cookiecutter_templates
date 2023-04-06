import os
import shlex
import subprocess
import sys
from pathlib import Path

import rich
import typer
from bx_py_utils.path import assert_is_dir, assert_is_file
from darker.__main__ import main as darker_main
from flake8.main.cli import main as flake8_main
from rich import print  # noqa

import your_cool_package
from your_cool_package import __version__


PACKAGE_ROOT = Path(your_cool_package.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT)
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')

app = typer.Typer(
    name='./cli.py',
    epilog='Project Homepage: https://github.com/john-doh/your_cool_package',
)


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
    venv_path = Path(sys.executable).parent
    assert_is_file(venv_path / 'flake8')
    assert_is_file(venv_path / 'darker')
    venv_path = str(venv_path)
    if venv_path not in os.environ['PATH']:
        os.environ['PATH'] = venv_path + os.pathsep + os.environ['PATH']

    print(f'Run "darker {shlex.join(str(part) for part in argv)}"...')
    exit_code = darker_main(argv=argv)
    print(f'darker exit code: {exit_code!r}')
    return exit_code


@app.command()
def fix_code_style():
    """
    Fix code style via darker
    """
    exit_code = _call_darker(argv=['--color'])
    sys.exit(exit_code)


@app.command()
def check_code_style(verbose: bool = True):
    darker_exit_code = _call_darker(argv=['--color', '--check'])
    if verbose:
        argv = ['--verbose']
    else:
        argv = []

    print(f'Run flake8 {shlex.join(str(part) for part in argv)}')
    flake8_exit_code = flake8_main(argv=argv)
    print(f'flake8 exit code: {flake8_exit_code!r}')
    sys.exit(max(darker_exit_code, flake8_exit_code))


@app.command()
def mypy(verbose: bool = True):
    """Run Mypy (configured in pyproject.toml)"""
    args = [which('mypy')]
    if verbose:
        args.append('--verbose')  # type: ignore[arg-type]
    verbose_check_call(*args, PACKAGE_ROOT)


@app.command()  # Just add this command to help page
def test():
    """
    Run unittests
    """
    args = sys.argv[2:]
    if not args:
        args = ('--verbose', '--locals', '--buffer')
    # Use the CLI from unittest module and pass all args to it:
    verbose_check_call(sys.executable, '-m', 'unittest', *args)


@app.command()
def coverage():
    """
    Run and show coverage.
    """
    coverage_bin = which('coverage')
    verbose_check_call(coverage_bin, 'run')
    verbose_check_call(coverage_bin, 'combine', '--append')
    verbose_check_call(coverage_bin, 'report', '--fail-under=30')
    verbose_check_call(coverage_bin, 'xml')
    verbose_check_call(coverage_bin, 'json')


@app.command()
def version(no_color: bool = False):
    """Print version and exit"""
    if no_color:
        rich.reconfigure(no_color=True)

    print(f'your_cool_package v{__version__}')


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        # Just use the CLI from unittest with all available options and origin --help output ;)
        return test()
    else:
        app()
