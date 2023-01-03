import logging
import os
import shlex
import shutil
import sys
from pathlib import Path

import rich
import typer
from bx_py_utils.path import assert_is_dir, assert_is_file
from darker.__main__ import main as darker_main
from flake8.main.cli import main as flake8_main
from manageprojects.git import Git
from manageprojects.utilities.subprocess_utils import verbose_check_call
from rich import print  # noqa

from managetemplates import __version__
from managetemplates.constants import PACKAGE_ROOT, REQ_DEV_TXT_PATH, REQ_TXT_PATH


logger = logging.getLogger(__name__)


app = typer.Typer()


@app.command()
def coverage(verbose: bool = True):
    """
    Run and show coverage.
    """
    verbose_check_call('coverage', 'run', verbose=verbose, exit_on_error=True, timeout=15 * 60)
    verbose_check_call('coverage', 'report', '--fail-under=50', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=True)


@app.command()
def install():
    """
    Run pip-sync and install 'managetemplates' via pip as editable.
    """
    verbose_check_call('pip-sync', REQ_DEV_TXT_PATH)
    verbose_check_call('pip', 'install', '-e', '.')


@app.command()
def update():
    """
    Update the development environment
    """
    extra_env = dict(
        CUSTOM_COMPILE_COMMAND='./cli.py update',
    )
    bin_path = Path(sys.executable).parent

    pip_compile_base = [
        bin_path / 'pip-compile',
        '--verbose',
        '--allow-unsafe',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
        '--resolver=backtracking',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
        '--upgrade',
        '--generate-hashes',
    ]

    ############################################################################
    # Update own dependencies:

    # Only "prod" dependencies:
    verbose_check_call(
        *pip_compile_base,
        'pyproject.toml',
        '--output-file',
        REQ_TXT_PATH,
        extra_env=extra_env,
    )
    # dependencies + "tests"-optional-dependencies:
    verbose_check_call(
        *pip_compile_base,
        'pyproject.toml',
        '--extra=tests',
        '--output-file',
        REQ_DEV_TXT_PATH,
        extra_env=extra_env,
    )

    ############################################################################
    # Update 'piptools-python' template:
    #   piptools-python/{{cookiecutter.package_name}}/requirements*.txt

    package_path = PACKAGE_ROOT / 'piptools-python' / '{{cookiecutter.package_name}}'
    assert_is_dir(package_path)

    verbose_check_call(  # develop + production
        *pip_compile_base,
        'pyproject.toml',
        '--output-file',
        package_path / 'requirements.txt',
        extra_env=extra_env,
    )

    verbose_check_call(  # production only
        *pip_compile_base,
        'pyproject.toml',
        '--extra=tests',
        '--output-file',
        package_path / 'requirements.dev.txt',
        extra_env=extra_env,
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
    venv_path = Path(sys.executable).parent
    assert_is_file(venv_path / 'flake8')
    assert_is_file(venv_path / 'darker')
    venv_path = str(venv_path)
    if venv_path not in os.environ['PATH']:
        os.environ['PATH'] = venv_path + os.pathsep + os.environ['PATH']

    print('_' * 100)
    print(f'Run "darker {shlex.join(str(part) for part in argv)}"...')
    exit_code = darker_main(argv=argv)
    print(f'\ndarker exit code: {exit_code!r}\n')
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

    print('_' * 100)
    print(f'Run "flake8 {shlex.join(str(part) for part in argv)}"...')
    flake8_exit_code = flake8_main(argv=argv)
    print(f'\nflake8 exit code: {flake8_exit_code!r}\n')
    sys.exit(max(darker_exit_code, flake8_exit_code))


@app.command()  # Just add this command to help page
def test():
    """
    Run unittests
    """
    args = sys.argv[2:]
    if not args:
        args = ('--verbose', '--locals', '--buffer')
    # Use the CLI from unittest module and pass all args to it:
    verbose_check_call(
        sys.executable,
        '-m',
        'unittest',
        *args,
        timeout=15 * 60,
        extra_env=dict(
            PYTHONUNBUFFERED='1',
            PYTHONWARNINGS='always',
        ),
    )


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        # Just use the CLI from unittest with all available options and origin --help output ;)
        return test()
    else:
        # Execute Typer App:
        app()
