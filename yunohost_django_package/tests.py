import json

import django_example
from bx_py_utils.path import assert_is_file

from managetemplates.constants import PACKAGE_ROOT
from managetemplates.tests.base import PackageTestBase, TempGitRepo


class YunohostDjangoPackageTemplateTestCase(PackageTestBase):
    template_name = 'yunohost_django_package'
    pkg_name = 'django_example_ynh'

    def test_basic(self):
        # The project used https://github.com/jedie/django_example
        # That is a real package on PyPi:
        # https://pypi.org/project/django-example/
        #
        # We have to use the real PyPi Version:
        cookiecutter_json_path = PACKAGE_ROOT / 'yunohost_django_package' / 'cookiecutter.json'
        assert_is_file(cookiecutter_json_path)
        raw_context = json.loads(cookiecutter_json_path.read_text(encoding='UTF-8'))
        if raw_context['upstream_version'] != django_example.__version__:
            raw_context['upstream_version'] = django_example.__version__
            content = json.dumps(raw_context, ensure_ascii=False, indent=4)
            cookiecutter_json_path.write_text(content, encoding='UTF-8')

        with TempGitRepo(path=self.pkg_path, fresh=True, branch_name='master') as temp_git:
            dev_cli_path = self.pkg_path / 'dev-cli.py'
            assert_is_file(dev_cli_path)

            req_txt = self.pkg_path / 'conf' / 'requirements.txt'
            assert_is_file(req_txt)

            output = self.test_project.check_output('python', 'dev-cli.py')
            self.assertIn('Usage: ./dev-cli.py [OPTIONS] COMMAND [ARGS]...', output)

            venv_path = self.pkg_path / '.venv'
            assert_is_file(venv_path / 'bin' / 'python')
            assert_is_file(venv_path / 'bin' / 'pip')
            assert_is_file(venv_path / 'bin' / 'django-admin')
            assert_is_file(venv_path / 'bin' / 'darker')
            assert_is_file(venv_path / 'bin' / 'black')

            self.test_project.check_call(
                'python',
                'dev-cli.py',
                'test',
                extra_env=dict(
                    # The project used snapshot tests,
                    # because of very small differences,
                    # they do not match :(
                    RAISE_SNAPSHOT_ERRORS='false',  # Don't raise snapshot errors
                    GITHUB_ACTION='1',  # Don't try to check the github upstream version
                ),
            )

            # The project unittests checks also the code style and tries to fix them,
            # in this case, we have a code difference:
            temp_git.assert_no_git_diff()
