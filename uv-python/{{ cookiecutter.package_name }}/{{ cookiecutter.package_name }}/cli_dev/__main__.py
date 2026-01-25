"""
    Allow {{ cookiecutter.package_name }} to be executable
    through `python -m {{ cookiecutter.package_name }}.cli_dev`.
"""

from {{ cookiecutter.package_name }}.cli_dev import main


if __name__ == '__main__':
    main()
