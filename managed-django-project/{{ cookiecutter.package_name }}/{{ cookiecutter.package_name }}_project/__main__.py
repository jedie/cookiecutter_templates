"""
    Allow {{ cookiecutter.package_name }} to be executable
    through `python -m {{ cookiecutter.package_name }}`.
"""
from pathlib import Path

from manage_django_project.config import ManageConfig
from manage_django_project.manage import execute_django_from_command_line

import {{ cookiecutter.package_name }}
import {{ cookiecutter.package_name }}_project


def main():
    """
    entrypoint installed via pyproject.toml and [project.scripts] section.
    Must be set in ./manage.py and PROJECT_SHELL_SCRIPT
    """
    execute_django_from_command_line(
        config=ManageConfig(
            module={{ cookiecutter.package_name }}_project,
            project_root_path=Path({{ cookiecutter.package_name }}.__file__).parent.parent,
            local_settings='{{ cookiecutter.package_name }}_project.settings.local',
            test_settings='{{ cookiecutter.package_name }}_project.settings.tests',
        )
    )


if __name__ == '__main__':
    main()
