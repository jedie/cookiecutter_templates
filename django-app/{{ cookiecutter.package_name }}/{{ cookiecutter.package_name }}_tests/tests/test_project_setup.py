import os
import shutil
import subprocess
from pathlib import Path

import tomli
from bx_py_utils.path import assert_is_dir, assert_is_file
from django.test import SimpleTestCase

import {{ cookiecutter.package_name }}
from {{ cookiecutter.package_name }} import __version__


PACKAGE_ROOT = Path({{ cookiecutter.package_name }}.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT)
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')


def _call_make(*args):
    make_bin = shutil.which('make')
    assert make_bin
    return subprocess.check_output(
        (make_bin,) + args,
        text=True,
        env=dict(PATH=os.environ['PATH']),
        stderr=subprocess.STDOUT,
        cwd=str(PACKAGE_ROOT),
    )


def poetry_check_output(*args):
    poerty_bin = shutil.which('poetry')

    output = subprocess.check_output(
        (poerty_bin,) + args,
        text=True,
        env=os.environ,
        stderr=subprocess.STDOUT,
        cwd=str(PACKAGE_ROOT),
    )
    return output


class ProjectSetupSimpleTestCase(SimpleTestCase):
    def test_version(self):
        pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
        pyproject_toml = tomli.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
        pyproject_version = pyproject_toml['tool']['poetry']['version']
        self.assertEqual(pyproject_version, __version__)

    def test_poetry_check(self):
        output = poetry_check_output('check')
        self.assertEqual(output, 'All set!\n', output)

    def test_check_code_style(self):
        # First try:
        try:
            _call_make('lint')
        except subprocess.CalledProcessError:
            # Fix and test again:
            try:
                _call_make('fix-code-style')
                _call_make('lint')
            except subprocess.CalledProcessError as err:
                raise AssertionError(f'Linting error:\n{"-"*100}\n{err.stdout}\n{"-"*100}')
