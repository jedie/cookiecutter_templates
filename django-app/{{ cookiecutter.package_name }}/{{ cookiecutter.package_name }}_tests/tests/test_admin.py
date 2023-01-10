from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.contrib.auth.models import User
from django.test import TestCase


class AdminTestCase(HtmlAssertionMixin, TestCase):
    def test_permissions(self):
        # Anonymous user redirect to login page:
        response = self.client.get('/admin/')
        self.assertRedirects(response, expected_url='/admin/login/?next=/admin/')

        # Super user can use the view:
        superuser = User.objects.create_superuser(username='a-superuser', password='ThisIsNotAPassword!')
        self.client.force_login(superuser)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assert_html_parts(
            response,
            parts=('<title>Site administration | Django site admin</title>',),
        )
