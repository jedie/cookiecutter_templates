import logging
import os
import shutil
from collections.abc import Iterable
from pathlib import Path
from unittest import TestCase

from bx_py_utils.path import assert_is_dir, assert_is_file
from cli_base.cli_tools.git import Git
from cli_base.cli_tools.test_utils.git_utils import init_git

from managetemplates.constants import ALL_TEMPLATES
from managetemplates.utilities.sync_cookiecutter_templates import cookiecutter_templates2generated
from managetemplates.utilities.test_project_utils import TestProject


class TempGitRepo:
    def __init__(self, path, fresh=False, branch_name='main'):
        assert_is_dir(path)
        self.path = path
        self.fresh = fresh
        self.git_path = path / '.git'

        self.branch_name = branch_name

        self.git = None

    def __enter__(self):
        if self.fresh and self.git_path.is_dir():
            shutil.rmtree(self.git_path)

        self.git, git_hash = init_git(path=self.path, branch_name=self.branch_name)
        return self

    def display_git_diff(self):
        output = self.git.git_verbose_output('diff')
        if not output:
            print('Git diff is empty -> nothing changed!')
        else:
            print('=' * 100)
            print(output)
            print('=' * 100)

    def assert_no_git_diff(self):
        output = self.git.git_verbose_output('diff')
        if not output:
            # Git diff is empty -> OK
            return

        raise AssertionError(f'Git diff:\n{"=" * 100}\n{output}\n{"=" * 100}\n')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.git_path.is_dir():
            shutil.rmtree(self.git_path)


class BaseTestCase(TestCase):
    maxDiff = None

    def init_git(self, pkg_path: Path) -> Git:
        assert_is_dir(pkg_path)
        git_path = pkg_path / '.git'

        if git_path.is_dir():
            # Start tests always with a fresh git
            shutil.rmtree(git_path)

        git, git_hash = init_git(path=pkg_path)  # Helpful to display diffs, see below ;)

        return git

    def assert_in(self, member, container, msg=None):
        try:
            self.assertIn(member, container, msg)
        except AssertionError:
            print('-' * 100)
            print(container)
            print('-' * 100)
            raise

    def assert_in_content(self, *, got: str, parts: Iterable[str]):
        assert parts
        missing_parts = [part for part in parts if part not in got]
        if missing_parts:
            print('-' * 79)
            print(got)
            print('-' * 79)
            info = ', '.join(repr(part) for part in missing_parts)
            raise AssertionError(f'Text parts: {info} not found in: {got!r}')

    def assert_is_executeable(self, file_path):
        assert_is_file(file_path)
        if not os.access(file_path, os.F_OK | os.X_OK):
            raise AssertionError(f'File {file_path} is not executeable!')


class PackageTestBase(BaseTestCase):
    template_name: str = None
    pkg_name: str = None
    base_extra_env = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        assert cls.template_name is not None
        assert cls.template_name in ALL_TEMPLATES, f'Template name {cls.template_name!r} not in {ALL_TEMPLATES}'

    def setUp(self) -> None:
        super().setUp()
        with self.assertLogs('cookiecutter', level=logging.DEBUG) as logs:
            self.pkg_path = cookiecutter_templates2generated(
                # force_recreate=True
                force_recreate=False,
                only_template=self.template_name,
            )
        self.assert_in_content(
            got='\n'.join(logs.output),
            parts=(
                f'{self.template_name}/cookiecutter.json',
                f'/{self.pkg_name}/',
                'Writing contents to file',
            ),
        )
        self.test_project = TestProject(self.pkg_path, base_extra_env=self.base_extra_env)
