import os
from collections.abc import Iterable
from unittest import TestCase

from bx_py_utils.path import assert_is_file
from manageprojects.git import Git


class BaseTestCase(TestCase):
    maxDiff = None

    def assert_no_git_diff(self, git: Git):
        output = git.git_verbose_output('diff')
        if not output:
            # Git diff is empty -> OK
            return

        raise AssertionError(f'Git diff:\n{"=" * 100}\n{output}\n{"=" * 100}\n')

    def display_git_diff(self, git: Git):
        output = git.git_verbose_output('diff')
        if not output:
            print('Git diff is empty -> nothing changed!')
        else:
            print('=' * 100)
            print(output)
            print('=' * 100)

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
