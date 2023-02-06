from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker


class ProjectSetupTestCase(HtmlAssertionMixin, TestCase):
    def test_admin(self):
        response = self.client.get('/admin/')
        self.assertRedirects(response, expected_url='/admin/login/?next=/admin/')

        UserModel = get_user_model()
        user = baker.make(UserModel, is_staff=True, is_active=True, is_superuser=True)
        self.client.force_login(user)

        with self.settings(DEBUG=True):
            response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='admin/index.html')
        self.assert_html_parts(
            response,
            parts=(
                '<title>Site administration | Django site admin</title>',
                '<link rel="stylesheet" href="/static/debug_toolbar/css/toolbar.css">',
            ),
        )
