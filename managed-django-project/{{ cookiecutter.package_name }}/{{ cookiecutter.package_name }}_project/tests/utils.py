import shutil
from pathlib import Path
from unittest import TestCase

# https://github.com/{{ cookiecutter.github_username }}/django-tools
from django_tools.unittest_utils.django_command import DjangoCommandMixin


class ForRunnersCommandTestCase(DjangoCommandMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        # installed via setup.py entry points !
        cls.{{ cookiecutter.package_name }}_bin = shutil.which("{{ cookiecutter.package_name }}")
        cls.manage_bin = shutil.which("manage")

    def _call_{{ cookiecutter.package_name }}(self, cmd, **kwargs):
        {{ cookiecutter.package_name }}_path = Path(self.{{ cookiecutter.package_name }}_bin)
        return self.call_manage_py(
            cmd=cmd,
            manage_dir=str({{ cookiecutter.package_name }}_path.parent),
            manage_py={{ cookiecutter.package_name }}_path.name,  # Python 3.5 needs str()
            **kwargs
        )

    def _call_manage(self, cmd, **kwargs):
        manage_path = Path(self.manage_bin)
        return self.call_manage_py(
            cmd=cmd,
            manage_dir=str(manage_path.parent),
            manage_py=manage_path.name,  # Python 3.5 needs str()
            **kwargs
        )
