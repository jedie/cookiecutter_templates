import logging
from pathlib import Path

from bx_py_utils.path import assert_is_file
from manageprojects.git import Git
from manageprojects.test_utils.git_utils import init_git

from managetemplates.tests.base import BaseTestCase
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter
from managetemplates.utilities.test_project_utils import TestProject


class ManagedDjangoProjectTemplateTestCase(BaseTestCase):
    def test_basic(self):
        with self.assertLogs('cookiecutter', level=logging.DEBUG) as logs:
            pkg_path: Path = run_cookiecutter(
                template_name='managed-django-project',
                final_name='your_cool_package',  # {{ cookiecutter.package_name }} replaced!
                # force_recreate=True
                force_recreate=False,
            )
        self.assert_in_content(
            got='\n'.join(logs.output),
            parts=(
                'managed-django-project/cookiecutter.json',
                'Writing contents to file',

            ),
        )
        test_project = TestProject(pkg_path)

        git_path = pkg_path / '.git'
        if not git_path.is_dir():
            # Newly generated -> git init
            git, git_hash = init_git(path=pkg_path)  # Helpful to display diffs, see below ;)
        else:
            # Reuse existing .git
            git = Git(cwd=git_path)

        manage_bin = pkg_path / 'manage.py'
        self.assert_is_executeable(manage_bin)

        ############################################################################
        # Bootstrap by call the ./manage.py

        output = test_project.check_output(manage_bin, 'version')
        self.assert_in('your_cool_package_project v0.0.1', output)

        assert_is_file(pkg_path / '.venv' / 'bin' / 'pip')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'python')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'tox')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'pip-compile')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'pip-sync')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'darker')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'flake8')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'coverage')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'twine')
        assert_is_file(pkg_path / '.venv' / 'bin' / 'your_cool_package_project')

        output = test_project.check_output(manage_bin, '--help')
        self.assert_in('Available subcommands:', output)
        self.assert_in('[django]', output)
        self.assert_in('runserver', output)
        self.assert_in('[manage_django_project]', output)

        output = test_project.check_output(manage_bin, 'code_style')
        self.assert_in('Code style: OK', output)

        # TODO:
        # output = test_project.check_output(manage_bin, 'test')
        # self.assert_in('Ran 4 tests', output)

        # The project unittests checks also the code style and tries to fix them,
        # in this case, we have a code difference:
        self.assert_no_git_diff(git=git)
