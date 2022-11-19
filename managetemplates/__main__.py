"""
    Allow managetemplates to be executable
    through `python -m managetemplates`.
"""


from managetemplates.cli import cli_app


def main():
    cli_app.main()


if __name__ == '__main__':
    main()
