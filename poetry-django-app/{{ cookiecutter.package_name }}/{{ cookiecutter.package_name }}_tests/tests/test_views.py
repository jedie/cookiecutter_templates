from django.test import TestCase
from django.urls import reverse

from {{ cookiecutter.package_name }} import __version__
from {{ cookiecutter.package_name }}.views import hello_world


class ViewsTestCase(TestCase):
    def test_hello_world(self):
        url = reverse(hello_world)
        self.assertEqual(url, '/hello_world')

        response = self.client.get('/hello_world')
        self.assertEqual(response.resolver_match.func, hello_world)
        self.assertEqual(
            response.content.decode('UTF-8'),
            f'Hello, world! From {{ cookiecutter.package_name }} v{__version__}',
        )
