from bx_py_utils.test_utils.unittest_utils import BaseDocTests

import {{ cookiecutter.ynh_app_pkg_name }}


class DocTests(BaseDocTests):
    def test_doctests(self):
        self.run_doctests(
            modules=({{ cookiecutter.ynh_app_pkg_name }},),
        )
