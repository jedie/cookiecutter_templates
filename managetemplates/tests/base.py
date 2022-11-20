import os
from unittest import TestCase

from bx_py_utils.path import assert_is_file
from manageprojects.git import Git


class BaseTestCase(TestCase):
    maxDiff = None

    def display_git_diff(self, git: Git):
        print('=' * 100)
        output = git.git_verbose_output('diff')
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

    def assert_is_executeable(self, file_path):
        assert_is_file(file_path)
        if not os.access(file_path, os.F_OK | os.X_OK):
            raise AssertionError(f'File {file_path} is not executeable!')
