import logging

from cli_base.cli_tools.dev_tools import run_unittest_cli
from cli_base.cli_tools.subprocess_utils import ToolsExecutor
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.run_pip_audit import run_pip_audit
from cli_base.tyro_commands import TyroVerbosityArgType
from django_yunohost_integration.path_utils import get_project_root
from manageprojects.utilities.publish import publish_package

import django_example_ynh
from django_example_ynh.cli_dev import app


logger = logging.getLogger(__name__)


@app.command
def install():
    """
    Install requirements and 'django_example_ynh' via pip as editable.
    """
    tools_executor = ToolsExecutor(cwd=get_project_root())
    tools_executor.verbose_check_call('uv', 'sync')
    tools_executor.verbose_check_call('pip', 'install', '--no-deps', '-e', '.')


@app.command
def pip_audit(verbosity: TyroVerbosityArgType):
    """
    Run pip-audit check against current requirements files
    """
    setup_logging(verbosity=verbosity)
    run_pip_audit(base_path=get_project_root(), verbosity=verbosity)


@app.command
def update(verbosity: TyroVerbosityArgType):
    """
    Update "requirements*.txt" dependencies files
    """
    setup_logging(verbosity=verbosity)

    tools_executor = ToolsExecutor(cwd=get_project_root())
    tools_executor.verbose_check_call('pip', 'install', '-U', 'pip')
    tools_executor.verbose_check_call('pip', 'install', '-U', 'uv')
    tools_executor.verbose_check_call('uv', 'lock', '--upgrade')

    run_pip_audit(base_path=get_project_root(), verbosity=verbosity)

    # Install new dependencies in current .venv:
    tools_executor.verbose_check_call('uv', 'sync')

    # Update conf/requirements.txt
    tools_executor.verbose_check_call(
        'uv',
        'export',
        '--no-header',
        '--frozen',
        '--no-editable',
        '--no-emit-project',
        '--no-dev',
        '-o',
        'conf/requirements.txt',
    )


@app.command
def publish():
    """
    Build and upload this project to PyPi
    """
    run_unittest_cli(verbose=False, exit_after_run=False)  # Don't publish a broken state

    publish_package(module=django_example_ynh, package_path=get_project_root())
