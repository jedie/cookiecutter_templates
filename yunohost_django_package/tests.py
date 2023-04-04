import logging
import shutil
from pathlib import Path

import django_example
from bx_py_utils.path import assert_is_file
from manageprojects.test_utils.git_utils import init_git

from managetemplates.tests.base import BaseTestCase
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter
from managetemplates.utilities.test_project_utils import TestProject


class YunohostDjangoPackageTemplateTestCase(BaseTestCase):
    def test_basic(self):
        with self.assertLogs('cookiecutter', level=logging.DEBUG) as logs:
            pkg_path: Path = run_cookiecutter(
                template_name='yunohost_django_package',
                final_name='django_example_ynh',  # {{ cookiecutter.ynh_app_pkg_name }} replaced!
                # force_recreate=True,
                force_recreate=False,
                extra_context=dict(
                    # Some projects test depends on the current upstream version
                    # So we have to set these version correct here:
                    upstream_version=django_example.__version__,
                    # We must use the correct Github urls:
                    upstream_url='https://github.com/jedie/django_example',
                ),
            )
        self.assert_in_content(
            got='\n'.join(logs.output),
            parts=(
                'yunohost_django_package/cookiecutter.json',
                'Writing contents to file',
            ),
        )
        test_project = TestProject(pkg_path)

        makefile_path = pkg_path / 'Makefile'
        assert_is_file(makefile_path)

        # must be a "git clone", because of darker ;)
        git_path = pkg_path / '.git'
        if git_path.is_dir():
            shutil.rmtree(git_path)

        poetry_lock = pkg_path / 'poetry.lock'
        req_txt = pkg_path / 'conf' / 'requirements.txt'
        if not (poetry_lock.is_file() and req_txt.is_file()):
            output = test_project.check_output('make', 'update')
            self.assert_in('poetry install', output)

        venv_path = pkg_path / '.venv'
        if not venv_path.is_dir():
            output = test_project.check_output('make', 'install')
            self.assert_in('poetry install', output)
            self.assert_in('Installing django-example', output)
            self.assert_in('Installing django-yunohost-integration', output)

        assert_is_file(venv_path / 'bin' / 'python')
        assert_is_file(venv_path / 'bin' / 'pip')
        assert_is_file(venv_path / 'bin' / 'django-admin')
        assert_is_file(venv_path / 'bin' / 'darker')
        assert_is_file(venv_path / 'bin' / 'black')

        # Newly generated -> git init (For darker)
        git, git_hash = init_git(
            path=pkg_path,
            branch_name='master',  # YunoHost apps doesn't switch to "main", yet :(
        )

        test_project.check_call(
            'make',
            'pytest',
            extra_env=dict(
                # The project used snapshot tests,
                # because of very small differences,
                # they do not match :(
                RAISE_SNAPSHOT_ERRORS='false'  # Don't raise snapshot errors
            ),
        )
