import shutil
from pathlib import Path

from bx_py_utils.path import assert_is_file
from cookiecutter.generate import generate_context
from cookiecutter.prompt import prompt_for_config
from manageprojects.cookiecutter_generator import create_cookiecutter_template
from manageprojects.utilities.temp_path import TemporaryDirectory
from rich import print  # noqa

from managetemplates import constants


def get_cookiecutter_context(src_path: Path) -> dict:
    cookiecutter_json_path = src_path / 'cookiecutter.json'
    print(f'Use context from: {cookiecutter_json_path}')
    assert_is_file(cookiecutter_json_path)

    context = generate_context(
        context_file=cookiecutter_json_path,
        default_context=None,
        extra_context=None,
    )

    # This will "resolve" all templates in context values:
    context = prompt_for_config(context, no_input=True)

    cookiecutter_context = {f'cookiecutter.{key}': value for key, value in context.items()}

    return dict(cookiecutter_context)


def reverse_test_project(pkg_name: str) -> None:
    test_path = constants.TEST_PATH / pkg_name
    src_path = constants.PACKAGE_ROOT / pkg_name

    print(f'Reverse {test_path} to Cookiecutter template here: {src_path}')

    cookiecutter_context = get_cookiecutter_context(src_path)
    assert cookiecutter_context, f'No cookiecutter context found here: {src_path}'

    with TemporaryDirectory(prefix=f'{pkg_name}_', cleanup=True) as temp_dir:
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
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(item, dst_path)
            else:
                print(f'Ignore non-file: {item}')

        print('-' * 100)

    print('\ndone.')
