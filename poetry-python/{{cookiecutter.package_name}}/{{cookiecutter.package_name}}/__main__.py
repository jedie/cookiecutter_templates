"""
    Allow {{ cookiecutter.package_name }} to be executable
    through `python -m {{ cookiecutter.package_name }}`.
"""
from {{ cookiecutter.package_name }} import cli


def main():
    cli.main()


if __name__ == '__main__':
    main()
