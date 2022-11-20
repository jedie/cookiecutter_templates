import logging
import os
import shlex
import shutil
import sys

import rich
import typer
from bx_py_utils.path import assert_is_dir, assert_is_file
from darker.__main__ import main as darker_main
from flake8.main.cli import main as flake8_main
from rich import print  # noqa

from managetemplates import __version__
from managetemplates.cli.git_utils import Git
from managetemplates.cli.subprocess_utils import verbose_check_call
from managetemplates.constants import PACKAGE_ROOT, REQ_IN_PATH, REQ_TXT_PATH


logger = logging.getLogger(__name__)


app = typer.Typer()


@app.command()
def coverage(verbose: bool = True):
    """
    Run and show coverage.
    """
    verbose_check_call('coverage', 'run', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'report', '--fail-under=50', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=True)


@app.command()
def install():
    """
    Run pip-sync and install 'managetemplates' via pip as editable.
    """
    verbose_check_call('pip-sync', REQ_TXT_PATH)
    verbose_check_call('pip', 'install', '-e', '.')


@app.command()
def update():
    """
    Update the development environment
    """

    verbose_check_call(  # develop + production
        'pip-compile',
        '--verbose',
        '--upgrade',
        '--allow-unsafe',
        '--generate-hashes',
        REQ_IN_PATH,
        '--output-file',
        REQ_TXT_PATH,
    )


@app.command()
def version(no_color: bool = False):
    """Print version and exit"""
    if no_color:
        rich.reconfigure(no_color=True)

    print(f'managetemplates v{__version__}')


@app.command()
def publish():
    """
    Build and upload this project to PyPi
    """
    test()  # Don't publish a broken state

    git = Git(cwd=PACKAGE_ROOT, detect_root=True)

    # TODO: Add the checks from:
    #       https://github.com/jedie/poetry-publish/blob/main/poetry_publish/publish.py

    dist_path = PACKAGE_ROOT / 'dist'
    if dist_path.exists():
        shutil.rmtree(dist_path)

    verbose_check_call(sys.executable, '-m', 'build')
    verbose_check_call('twine', 'check', 'dist/*')

    git_tag = f'v{__version__}'
    print('\ncheck git tag')
    git_tags = git.tag_list()
    if git_tag in git_tags:
        print(f'\n *** ERROR: git tag {git_tag!r} already exists!')
        print(git_tags)
        sys.exit(3)
    else:
        print('OK')

    verbose_check_call('twine', 'upload', 'dist/*')

    git.tag(git_tag, message=f'publish version {git_tag}')
    print('\ngit push tag to server')
    git.push(tags=True)


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

    print(f'Run darker {shlex.join(str(part) for part in argv)}')
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


@app.command()  # Just add this command to help page
def test():
    """
    Run unittests
    """
    # Use the CLI from unittest module and pass all args to it:
    verbose_check_call(sys.executable, '-m', 'unittest', *sys.argv[2:])


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        # Just use the CLI from unittest with all available options and origin --help output ;)
        return test()
    else:
        # Execute Typer App:
        app()
