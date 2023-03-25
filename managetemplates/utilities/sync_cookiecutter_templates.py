from pathlib import Path

from managetemplates.constants import ALL_TEMPLATES
from managetemplates.utilities.cookiecutter_utils import run_cookiecutter


def cookiecutter_templates2generated(force_recreate: bool = False) -> None:
    for template_name in ALL_TEMPLATES:
        print('_' * 100)
        print(template_name)
        pkg_path: Path = run_cookiecutter(
            template_name=template_name,
            force_recreate=force_recreate,
        )
        print(pkg_path)
