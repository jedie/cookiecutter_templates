from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker


class AdminAnonymousTests(HtmlAssertionMixin, TestCase):
    """
    Anonymous will be redirected to the login page.
    """

    def test_login_en(self):
        response = self.client.get("/en/admin/", HTTP_ACCEPT_LANGUAGE="en")
        self.assertRedirects(response, expected_url="/en/admin/login/?next=/en/admin/")

    def test_login_de(self):
        response = self.client.get("/de/admin/", HTTP_ACCEPT_LANGUAGE="de")
        self.assertRedirects(response, expected_url="/de/admin/login/?next=/de/admin/")


class AdminLoggedinTests(HtmlAssertionMixin, TestCase):
    """
    Some basics test with the django admin
    """

    @classmethod
    def setUpTestData(cls):
        cls.superuser = baker.make(
            User, username='superuser', is_staff=True, is_active=True, is_superuser=True
        )
        cls.staffuser = baker.make(
            User, username='staff_test_user', is_staff=True, is_active=True, is_superuser=False
        )

    def test_staff_admin_index(self):
        self.client.force_login(self.staffuser)

        response = self.client.get("/en/admin/", HTTP_ACCEPT_LANGUAGE="en")
        self.assert_html_parts(
            response,
            parts=(
                "<h1>Site administration</h1>",
                "<strong>staff_test_user</strong>",
                "<p>You don’t have permission to view or edit anything.</p>",
            ),
        )
        self.assertTemplateUsed(response, template_name="admin/index.html")

    def test_superuser_admin_index(self):
        self.client.force_login(self.superuser)
        response = self.client.get("/en/admin/", HTTP_ACCEPT_LANGUAGE="en")
        self.assert_html_parts(
            response,
            parts=(
                "<h1>Site administration</h1>",
                "<strong>superuser</strong>",
                "/admin/auth/group/add/",
                "/admin/auth/user/add/",
            ),
        )
        self.assertTemplateUsed(response, template_name="admin/index.html")
