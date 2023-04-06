import shutil
from pathlib import Path
from unittest import TestCase

# https://github.com/john-doh/django-tools
from django_tools.unittest_utils.django_command import DjangoCommandMixin


class ForRunnersCommandTestCase(DjangoCommandMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        # installed via setup.py entry points !
        cls.your_cool_package_bin = shutil.which("your_cool_package")
        cls.manage_bin = shutil.which("manage")

    def _call_your_cool_package(self, cmd, **kwargs):
        your_cool_package_path = Path(self.your_cool_package_bin)
        return self.call_manage_py(
            cmd=cmd,
            manage_dir=str(your_cool_package_path.parent),
            manage_py=your_cool_package_path.name,  # Python 3.5 needs str()
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
