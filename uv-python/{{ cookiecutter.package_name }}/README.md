# {{ cookiecutter.package_name }}

[![tests]({{ cookiecutter.package_url }}/actions/workflows/tests.yml/badge.svg?branch=main)]({{ cookiecutter.package_url }}/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}/branch/main/graph/badge.svg)](https://app.codecov.io/github/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }})
[![{{ cookiecutter.package_name }} @ PyPi](https://img.shields.io/pypi/v/{{ cookiecutter.package_name }}?label={{ cookiecutter.package_name }}%20%40%20PyPi)](https://pypi.org/project/{{ cookiecutter.package_name }}/)
[![Python Versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.package_name }})]({{ cookiecutter.package_url }}/blob/main/pyproject.toml)
[![License {{ cookiecutter.license }}](https://img.shields.io/pypi/l/{{ cookiecutter.package_name }})]({{ cookiecutter.package_url }}/blob/main/LICENSE)

{{ cookiecutter.package_description }}

## CLI

[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ update-readme-history      Update project history base on git commits/tags in README.md          │
│ version                    Print version and exit                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)


## dev CLI

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
Usage: ./dev-cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ check-code-style            Check code style by calling darker + flake8                          │
│ coverage                    Run tests and show coverage report.                                  │
│ fix-code-style              Fix code style of all {{ cookiecutter.package_name }} source code files via darker │
│ install                     Install requirements and '{{ cookiecutter.package_name }}' via pip as editable.    │
│ mypy                        Run Mypy (configured in pyproject.toml)                              │
│ pip-audit                   Run pip-audit check against current requirements files               │
│ publish                     Build and upload this project to PyPi                                │
│ test                        Run unittests                                                        │
│ tox                         Run tox                                                              │
│ update                      Update "requirements*.txt" dependencies files                        │
│ update-test-snapshot-files  Update all test snapshot files (by remove and recreate all snapshot  │
│                             files)                                                               │
│ version                     Print version and exit                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)


## History

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)



[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
