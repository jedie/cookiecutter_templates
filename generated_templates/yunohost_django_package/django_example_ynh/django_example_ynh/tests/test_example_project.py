import os

from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.conf import settings
from django.test.testcases import TestCase
from django.urls.base import reverse


class ExampleProjectTestCase(HtmlAssertionMixin, TestCase):
    def test_urls(self):
        assert settings.PATH_URL == 'app_path'
        assert reverse('admin:index') == '/app_path/admin/'
        assert reverse('debug-view') == '/app_path/'

        ###############################################################################
        # Test as anonymous user

        with self.assertLogs('django_example') as logs:
            response = self.client.get(
                path='/app_path/',
                secure=True,
            )
        self.assert_html_parts(
            response,
            parts=(
                '<li><a href="/app_path/admin/">Django Admin</a></li>',
                '<p>Log in to see more information</p>',
                '<tr><td>User:</td><td>AnonymousUser</td></tr>',
                '<tr><td>META:</td><td></td></tr>',
            ),
        )
        self.assertEqual(
            logs.output, ['INFO:django_example.views:DebugView request from user: AnonymousUser']
        )

        ###############################################################################
        # Test as SSO user

        self.client.cookies['SSOwAuthUser'] = 'test'

        with self.assertLogs('django_example') as logs:
            response = self.client.get(
                path='/app_path/',
                HTTP_REMOTE_USER='test',
                HTTP_AUTH_USER='test',
                HTTP_AUTHORIZATION='basic dGVzdDp0ZXN0MTIz',
                secure=True,
            )
        self.assert_html_parts(
            response,
            parts=(
                '<li><a href="/app_path/admin/">Django Admin</a></li>',
                '<tr><td>User:</td><td>test</td></tr>',
                f'<tr><td>Process ID:</td><td>{os.getpid()}</td></tr>',
            ),
        )
        self.assertEqual(
            logs.output, ['INFO:django_example.views:DebugView request from user: test']
        )
