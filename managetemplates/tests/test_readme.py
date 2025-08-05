from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRichClick, invoke
from manageprojects.tests.base import BaseTestCase

from managetemplates import constants
from managetemplates.constants import PACKAGE_ROOT


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
    README_PATH = PACKAGE_ROOT / 'README.md'
    assert_is_file(README_PATH)

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
        dir_name = entry.name
        if dir_name.startswith('.'):
            continue
        if dir_name in ('__pycache__', 'dist', 'generated_templates', 'managetemplates', 'managetemplates.egg-info'):
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
        with NoColorEnvRichClick():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'cli.py', args=['--help'], strip_line_prefix='usage: ')
        self.assert_in_content(
            got=stdout,
            parts=(
                'fix-file-content',
                'fix-filesystem',
                'reverse',
                'usage: ./cli.py [-h]',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='main help')

    def test_dev_help(self):
        with NoColorEnvRichClick():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'dev-cli.py', args=['--help'], strip_line_prefix='usage: ')
        self.assert_in_content(
            got=stdout,
            parts=(
                'usage: ./dev-cli.py [-h]',
                ' check-code-style ',
                ' coverage ',
                ' update-readme-history ',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='dev help')
