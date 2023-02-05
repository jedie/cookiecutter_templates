import logging
import os
import shutil
import sys
from pathlib import Path

import rich
import typer
from bx_py_utils.path import assert_is_dir, assert_is_file
from manageprojects.git import Git
from manageprojects.utilities.subprocess_utils import verbose_check_call
from rich import print  # noqa

import managetemplates
from managetemplates import __version__, constants
from managetemplates.utilities.reverse import reverse_test_project
from managetemplates.utilities.template_var_syntax import filesystem_template_var_syntax


logger = logging.getLogger(__name__)


PACKAGE_ROOT = Path(managetemplates.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT)
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')


app = typer.Typer(
    name='./cli.py',
    epilog='Project Homepage: https://github.com/jedie/cookiecutter_templates',
)


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
    verbose_check_call('pip-sync', constants.REQ_DEV_TXT_PATH)
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
        constants.REQ_TXT_PATH,
        extra_env=extra_env,
    )
    # dependencies + "dev"-optional-dependencies:
    verbose_check_call(
        *pip_compile_base,
        'pyproject.toml',
        '--extra=tests',
        '--output-file',
        constants.REQ_DEV_TXT_PATH,
        extra_env=extra_env,
    )

    ############################################################################
    # Update 'piptools-python' template:
    #   piptools-python/{{cookiecutter.package_name}}/requirements*.txt

    package_path = constants.PACKAGE_ROOT / 'piptools-python' / '{{cookiecutter.package_name}}'
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

    git = Git(cwd=constants.PACKAGE_ROOT, detect_root=True)

    # TODO: Add the checks from:
    #       https://github.com/jedie/poetry-publish/blob/main/poetry_publish/publish.py

    dist_path = constants.PACKAGE_ROOT / 'dist'
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


@app.command()
def fix_filesystem():
    """
    Unify cookiecutter variables in the filesystem. e.g.: "/{{foo}}/{{bar}}.txt" -> "/{{ foo }}/{{ bar }}.txt"
    """
    rename_count = filesystem_template_var_syntax(path=PACKAGE_ROOT)
    sys.exit(rename_count)


def _call_darker(*args):
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
        extra_env = dict(PATH=venv_path + os.pathsep + os.environ['PATH'])
    else:
        extra_env = None

    verbose_check_call(
        'darker',
        '--color',
        *args,
        cwd=PACKAGE_ROOT,
        extra_env=extra_env,
        exit_on_error=True,
    )


@app.command()
def fix_code_style(verbose: bool = False):
    """
    Fix code style via darker
    """
    if verbose:
        args = ['--verbose']
    else:
        args = []

    _call_darker(*args)
    print('Code style fixed, OK.')
    sys.exit(0)


@app.command()
def check_code_style(verbose: bool = False):
    if verbose:
        args = ['--verbose']
    else:
        args = []

    _call_darker('--check', *args)

    verbose_check_call(
        'flake8',
        *args,
        cwd=PACKAGE_ROOT,
        exit_on_error=True,
    )
    print('Code style: OK')
    sys.exit(0)


@app.command()
def reverse(pkg_name: str):
    """
    Reverse a /.tests/<pkg_name>/ back to Cookiecutter template in: ./<pkg_name>/
    """
    reverse_test_project(pkg_name=pkg_name)


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
