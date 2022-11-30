import re
from pathlib import Path
from unittest import TestCase

from bx_py_utils.path import assert_is_file
from bx_py_utils.test_utils.assertion import assert_text_equal

from managetemplates.constants import PACKAGE_ROOT


ADDITIONAL_TEMPLATE = '''
Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory %(template_name)s
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory %(template_name)s ~/foobar/
```
'''.strip()  # noqa:E501


def assert_readme(
    readme_path: Path,
    doc_block: str,
    start_marker_line: str = '[comment]: <> (✂✂✂ auto generated start ✂✂✂)',
    end_marker_line: str = '[comment]: <> (✂✂✂ auto generated end ✂✂✂)',
) -> None:
    """
    TODO: Move to bx_py_utils
    """
    assert readme_path.is_file()
    old_readme = readme_path.read_text()

    assert start_marker_line in old_readme
    assert end_marker_line in old_readme

    doc_block = f'{start_marker_line}\n{doc_block}\n{end_marker_line}'

    start = re.escape(start_marker_line)
    end = re.escape(end_marker_line)

    new_readme, sub_count = re.subn(f'{start}(.*?){end}', doc_block, old_readme, flags=re.DOTALL)
    assert sub_count == 1
    if old_readme != new_readme:
        readme_path.write_text(new_readme)

        # display error message with diff:
        assert_text_equal(old_readme, new_readme)


def get_template_paths():
    for entry in PACKAGE_ROOT.iterdir():
        if not entry.is_dir():
            continue
        if entry.name.startswith('.'):
            continue
        if entry.name in ('managetemplates', 'managetemplates.egg-info'):
            continue
        yield entry


def get_template_readmes(template_paths):
    result = {}
    for path in template_paths:
        readme_path = path / 'README.md'
        assert_is_file(readme_path)
        result[path.name] = readme_path
    return result


def build_readme_block(template_readmes):
    parts = []
    for template_name, readme_path in template_readmes.items():
        template_readme = readme_path.read_text()
        template_readme = template_readme.replace('# ', '## ')
        template_readme = template_readme.replace(' - CookieCutter template', '')
        parts.append(template_readme)

        additional = ADDITIONAL_TEMPLATE % {'template_name': template_name}
        parts.append(additional)

    return '\n\n'.join(parts)


class ReadmeTestCase(TestCase):
    def test_templates_doc(self):
        template_paths = sorted(get_template_paths())
        self.assertEqual(
            [path.name for path in template_paths],
            ['pipenv-python', 'piptools-python', 'poetry-python', 'yunohost_django_package'],
        )

        template_readmes = get_template_readmes(template_paths=template_paths)
        self.assertEqual(
            sorted(template_readmes.keys()),
            ['pipenv-python', 'piptools-python', 'poetry-python', 'yunohost_django_package'],
        )

        readme_block = build_readme_block(template_readmes)
        assert_readme(readme_path=PACKAGE_ROOT / 'README.md', doc_block=readme_block)
