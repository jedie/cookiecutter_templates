"""
    Allow managetemplates to be executable
    through `python -m managetemplates`.
"""
from managetemplates import cli


def main():
    cli.main()


if __name__ == '__main__':
    main()
