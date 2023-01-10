import json
import shutil
import sys
import tempfile
from pathlib import Path

from bx_py_utils.path import assert_is_dir, assert_is_file
from manageprojects.cookiecutter_generator import create_cookiecutter_template
from rich import print  # noqa

from managetemplates import constants


def resolve_test_path(test_path: Path) -> Path:
    if not test_path.is_dir():
        print(f'ERROR: Package {test_path.name!r} not found here: {test_path}')
        print('(Hint: Run tests first to create all packages!)')
        sys.exit(1)

    items = list(test_path.iterdir())
    if len(items) != 1:
        print(f'ERROR: {test_path} does not contains *one* directory: {items}')
        sys.exit(1)

    test_path = items[0]
    print(f'Use source files from: {test_path}')
    assert_is_dir(test_path)
    return test_path


def resolve_src_path(src_path: Path) -> Path:
    if not src_path.is_dir():
        print(f'ERROR: {src_path.name!r} is not an existing Cookiecutter template:')
        print(f'{src_path!r} does not exists.')
        sys.exit()

    items = [item for item in src_path.iterdir() if item.is_dir()]
    if len(items) != 1:
        print(f'ERROR: {src_path} does not contains *one* directory: {items}')
        sys.exit(1)

    src_path = items[0]
    print(f'Final destination: {src_path}')
    assert_is_dir(src_path)
    return src_path


def get_cookiecutter_context(src_path: Path) -> dict:
    cookiecutter_json_path = src_path / 'cookiecutter.json'
    print(f'Use context from: {cookiecutter_json_path}')
    assert_is_file(cookiecutter_json_path)
    cookiecutter_json = cookiecutter_json_path.read_text(encoding='UTF-8')
    context = json.loads(cookiecutter_json)
    cookiecutter_context = {'cookiecutter': context}
    return cookiecutter_context


def reverse_test_project(pkg_name: str) -> None:
    test_path = constants.PACKAGE_ROOT / '.tests' / pkg_name
    src_path = constants.PACKAGE_ROOT / pkg_name

    print(f'Reverse {test_path} to Cookiecutter template here: {src_path}')

    cookiecutter_context = get_cookiecutter_context(src_path)

    test_path = resolve_test_path(test_path)
    src_path = resolve_src_path(src_path)

    with tempfile.TemporaryDirectory(prefix=f'{pkg_name}_') as temp_dir:
        destination = Path(temp_dir) / pkg_name

        print('_' * 100)
        print('Reverse Cookiecutter template into temp directory:')

        create_cookiecutter_template(
            source_path=test_path,
            destination=destination,
            cookiecutter_context=cookiecutter_context,
        )

        print('_' * 100)
        print('Copy files from temp to final destination:')

        for item in destination.rglob('*'):
            if item.is_dir():
                continue
            elif item.is_file():
                dst_path = src_path / item.relative_to(destination)
                print(item, '->', dst_path)
                shutil.copy(item, dst_path)
            else:
                print(f'Ignore non-file: {item}')

        print('-' * 100)

    print('\ndone.')
