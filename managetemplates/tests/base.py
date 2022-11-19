from unittest import TestCase

from manageprojects.git import Git


class BaseTestCase(TestCase):
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
