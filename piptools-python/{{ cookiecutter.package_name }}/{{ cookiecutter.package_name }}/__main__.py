"""
    Allow {{ cookiecutter.package_name }} to be executable
    through `python -m {{ cookiecutter.package_name }}`.
"""


from {{ cookiecutter.package_name }}.cli import cli_app


def main():
    cli_app.main()


if __name__ == '__main__':
    main()
