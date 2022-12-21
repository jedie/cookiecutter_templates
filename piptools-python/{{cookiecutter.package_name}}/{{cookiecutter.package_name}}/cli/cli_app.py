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
from rich import print  # noqa

import {{ cookiecutter.package_name }}
from {{ cookiecutter.package_name }} import __version__
from {{cookiecutter.package_name}}.cli.subprocess_utils import verbose_check_call
from {{cookiecutter.package_name}}.cli.git_utils import Git


logger = logging.getLogger(__name__)


PACKAGE_ROOT = Path({{ cookiecutter.package_name }}.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT)
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')


app = typer.Typer()


@app.command()
def mypy(verbose: bool = True):
    """Run Mypy (configured in pyproject.toml)"""
    verbose_check_call('mypy', '.', cwd=PACKAGE_ROOT, verbose=verbose, exit_on_error=True)


@app.command()
def coverage(verbose: bool = True):
    """
    Run and show coverage.
    """
    verbose_check_call('coverage', 'run', verbose=verbose, exit_on_error=True)
    verbose_check_call(
        'coverage', 'report', '--fail-under=50', verbose=verbose, exit_on_error=True
    )
    verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=True)


@app.command()
def install():
    """
    Run pip-sync and install '{{ cookiecutter.package_name }}' via pip as editable.
    """
    verbose_check_call('pip-sync', PACKAGE_ROOT / 'requirements' / 'develop.txt')
    verbose_check_call('pip', 'install', '-e', '.')


@app.command()
def update():
    """
    Update the development environment by calling:
    - pip-compile production.in develop.in -> develop.txt
    - pip-compile production.in -> production.txt
    - pip-sync develop.txt
    """
    base_command = [
        'pip-compile',
        '--verbose',
        '--upgrade',
        '--allow-unsafe',
        '--generate-hashes',
        '--resolver=backtracking',
        'requirements/production.in',
    ]
    verbose_check_call(  # develop + production
        *base_command,
        'requirements/develop.in',
        '--output-file',
        'requirements/develop.txt',
    )
    verbose_check_call(  # production only
        *base_command,
        '--output-file',
        'requirements/production.txt',
    )
    verbose_check_call('pip-sync', 'requirements/develop.txt')


@app.command()
def version(no_color: bool = False):
    """Print version and exit"""
    if no_color:
        rich.reconfigure(no_color=True)

    print(f'{{ cookiecutter.package_name }} v{__version__}')


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
