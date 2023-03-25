"""
    Allow your_cool_package to be executable
    through `python -m your_cool_package`.
"""
from your_cool_package import cli


def main():
    cli.main()


if __name__ == '__main__':
    main()
