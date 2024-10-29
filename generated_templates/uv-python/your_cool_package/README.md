# your_cool_package

[![tests](https://github.com/john-doh/your_cool_package/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/john-doh/your_cool_package/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/john-doh/your_cool_package/branch/main/graph/badge.svg)](https://app.codecov.io/github/john-doh/your_cool_package)
[![your_cool_package @ PyPi](https://img.shields.io/pypi/v/your_cool_package?label=your_cool_package%20%40%20PyPi)](https://pypi.org/project/your_cool_package/)
[![Python Versions](https://img.shields.io/pypi/pyversions/your_cool_package)](https://github.com/john-doh/your_cool_package/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/your_cool_package)](https://github.com/john-doh/your_cool_package/blob/main/LICENSE)

A minimal Python package

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
│ fix-code-style              Fix code style of all your_cool_package source code files via darker │
│ install                     Install requirements and 'your_cool_package' via pip as editable.    │
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
