"""
    Allow {{ cookiecutter.package_name }} to be executable
    through `python -m {{ cookiecutter.package_name }}`.
"""


def main():
    print('Hello World from {{ cookiecutter.package_name }}')


if __name__ == '__main__':
    main()
