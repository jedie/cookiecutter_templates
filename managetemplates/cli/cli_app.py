# no:vars_cleanup

import logging
import shutil
import sys
from pathlib import Path

import rich_click as click
from bx_py_utils.path import assert_is_dir
from manageprojects.git import Git
from manageprojects.utilities import code_style
from manageprojects.utilities.subprocess_utils import verbose_check_call
from manageprojects.utilities.version_info import print_version
from rich import print  # noqa
from rich_click import RichGroup

import managetemplates
from managetemplates import __version__, constants
from managetemplates.utilities.reverse import reverse_test_project
from managetemplates.utilities.template_var_syntax import content_template_var_syntax, filesystem_template_var_syntax


logger = logging.getLogger(__name__)


OPTION_ARGS_DEFAULT_TRUE = dict(is_flag=True, show_default=True, default=True)
OPTION_ARGS_DEFAULT_FALSE = dict(is_flag=True, show_default=True, default=False)


class ClickGroup(RichGroup):  # FIXME: How to set the "info_name" easier?
    def make_context(self, info_name, *args, **kwargs):
        info_name = './cli.py'
        return super().make_context(info_name, *args, **kwargs)


@click.group(
    cls=ClickGroup,
    epilog=constants.CLI_EPILOG,
)
def cli():
    pass


@click.command()
def coverage(verbose: bool = True):
    """
    Run and show coverage.
    """
    verbose_check_call('coverage', 'run', verbose=verbose, exit_on_error=True, timeout=15 * 60)
    verbose_check_call('coverage', 'report', '--fail-under=50', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=True)


cli.add_command(coverage)


@click.command()
def install():
    """
    Run pip-sync and install 'managetemplates' via pip as editable.
    """
    verbose_check_call('pip-sync', constants.REQ_DEV_TXT_PATH)
    verbose_check_call('pip', 'install', '-e', '.')


cli.add_command(install)


@click.command()
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
    #   piptools-python/{{ cookiecutter.package_name }}/requirements*.txt

    package_path = constants.PACKAGE_ROOT / 'piptools-python' / '{{ cookiecutter.package_name }}'
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


cli.add_command(update)


@click.command()
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


cli.add_command(version)


@click.command()
def publish():
    """
    Build and upload this project to PyPi
    """
    _run_unittest_cli(verbose=False)  # Don't publish a broken state

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


cli.add_command(publish)


@click.command()
def fix_filesystem():
    """
    Unify cookiecutter variables in the file/directory paths.
    e.g.: "/{{foo}}/{{bar}}.txt" -> "/{{ foo }}/{{ bar }}.txt"
    """
    rename_count = filesystem_template_var_syntax(path=constants.PACKAGE_ROOT)
    sys.exit(rename_count)


cli.add_command(fix_filesystem)


@click.command()
def fix_file_content():
    """
    Unify cookiecutter variables in file content.
    e.g.: "{{foo}}" -> "{{ foo }}"
    """
    fixed_files = content_template_var_syntax(path=constants.PACKAGE_ROOT)
    sys.exit(fixed_files)


cli.add_command(fix_file_content)


@click.command()
@click.option('--color/--no-color', **OPTION_ARGS_DEFAULT_TRUE)
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def fix_code_style(color: bool = True, verbose: bool = False):
    """
    Fix code style via darker
    """
    code_style.fix(package_root=constants.PACKAGE_ROOT, color=color, verbose=verbose)


cli.add_command(fix_code_style)


@click.command()
@click.option('--color/--no-color', **OPTION_ARGS_DEFAULT_TRUE)
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def check_code_style(color: bool = True, verbose: bool = False):
    """
    Check code style by calling darker + flake8
    """
    code_style.check(package_root=constants.PACKAGE_ROOT, color=color, verbose=verbose)


cli.add_command(check_code_style)


@click.command()
@click.argument('pkg_name')
def reverse(pkg_name: str):
    """
    Reverse a /.tests/<pkg_name>/ back to Cookiecutter template in: ./<pkg_name>/
    """
    reverse_test_project(pkg_name=pkg_name)


cli.add_command(reverse)


def _run_unittest_cli(extra_env=None, verbose=True):
    """
    Call the origin unittest CLI and pass all args to it.
    """
    if extra_env is None:
        extra_env = dict()

    extra_env.update(
        dict(
            PYTHONUNBUFFERED='1',
            PYTHONWARNINGS='always',
        )
    )

    args = sys.argv[2:]
    if not args:
        if verbose:
            args = ('--verbose', '--locals', '--buffer')
        else:
            args = ('--locals', '--buffer')

    verbose_check_call(
        sys.executable,
        '-m',
        'unittest',
        *args,
        timeout=15 * 60,
        extra_env=extra_env,
    )


@click.command()  # Dummy command, to add "tests" into help page ;)
def test():
    """
    Run unittests
    """
    _run_unittest_cli()
    sys.exit(0)


cli.add_command(test)


def main():
    print_version(managetemplates)

    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        # Just use the CLI from unittest with all available options and origin --help output ;)
        _run_unittest_cli()
    else:
        # Execute Click CLI:
        cli.name = './cli.py'
        cli()
