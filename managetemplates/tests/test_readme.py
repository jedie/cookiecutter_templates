from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file
from manageprojects.test_utils.click_cli_utils import invoke_click
from manageprojects.tests.base import BaseTestCase

from managetemplates import constants
from managetemplates.cli.cli_app import cli
from managetemplates.constants import PACKAGE_ROOT


README_PATH = PACKAGE_ROOT / 'README.md'

ADDITIONAL_TEMPLATE = '''
Cookiecutter template tests are here: [%(tests_rel_path)s](https://github.com/jedie/cookiecutter_templates/blob/main/%(tests_rel_path)s)


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory %(template_name)s
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory %(template_name)s ~/foobar/
```
'''.strip()  # noqa:E501


def assert_cli_help_in_readme(text_block: str, marker: str):
    text_block = text_block.replace(constants.CLI_EPILOG, '')
    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=README_PATH,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


def get_template_paths():
    for entry in PACKAGE_ROOT.iterdir():
        if not entry.is_dir():
            continue
        if entry.name.startswith('.'):
            continue
        if entry.name in ('generated_templates', 'managetemplates', 'managetemplates.egg-info'):
            continue
        yield entry


def build_readme_block(template_paths):
    parts = []
    for path in template_paths:
        template_name = path.name

        readme_path = path / 'README.md'
        assert_is_file(readme_path)

        tests_path = path / 'tests.py'
        assert_is_file(tests_path)
        tests_rel_path = tests_path.relative_to(PACKAGE_ROOT)

        template_readme = readme_path.read_text()
        template_readme = template_readme.replace('# ', '## ')
        template_readme = template_readme.replace(' - CookieCutter template', '')
        parts.append(template_readme)

        additional = ADDITIONAL_TEMPLATE % {
            'template_name': template_name,
            'tests_rel_path': tests_rel_path,
        }
        parts.append(additional)

    return '\n\n'.join(parts)


class ReadmeTestCase(BaseTestCase):
    def test_templates_doc(self):
        template_paths = sorted(get_template_paths())
        self.assertEqual(
            tuple(path.name for path in template_paths),
            constants.ALL_TEMPLATES,
        )

        readme_block = build_readme_block(template_paths)
        assert_readme_block(readme_path=PACKAGE_ROOT / 'README.md', text_block=readme_block)

    def test_main_help(self):
        stdout = invoke_click(cli, '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...',
                'fix-file-content',
                'fix-filesystem',
                'reverse',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='main help')
