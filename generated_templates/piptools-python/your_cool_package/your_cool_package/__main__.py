"""
    Allow your_cool_package to be executable
    through `python -m your_cool_package`.
"""


from your_cool_package.cli import cli_app


def main():
    cli_app.main()


if __name__ == '__main__':
    main()
