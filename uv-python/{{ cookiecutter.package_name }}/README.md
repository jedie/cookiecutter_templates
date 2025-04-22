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
usage: ./cli.py [-h] {version}



╭─ options ─────────────────────────────────────────╮
│ -h, --help        show this help message and exit │
╰───────────────────────────────────────────────────╯
╭─ subcommands ─────────────────────────────────────╮
│ {version}                                         │
│     version       Print version and exit          │
╰───────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)


## dev CLI

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
usage: ./dev-cli.py [-h]
                    {check-code-style,coverage,fix-code-style,install,mypy,nox,pip-audit,publish,test,update,update-re
adme-history,update-test-snapshot-files,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ {check-code-style,coverage,fix-code-style,install,mypy,nox,pip-audit,publish,test,update,update-readme-history,upd │
│ ate-test-snapshot-files,version}                                                                                   │
│     check-code-style                                                                                               │
│                   Check code style by calling darker + flake8                                                      │
│     coverage      Run tests and show coverage report.                                                              │
│     fix-code-style                                                                                                 │
│                   Fix code style of all {{ cookiecutter.package_name }} source code files via darker                             │
│     install       Install requirements and '{{ cookiecutter.package_name }}' via pip as editable.                                │
│     mypy          Run Mypy (configured in pyproject.toml)                                                          │
│     nox           Run nox                                                                                          │
│     pip-audit     Run pip-audit check against current requirements files                                           │
│     publish       Build and upload this project to PyPi                                                            │
│     test          Run unittests                                                                                    │
│     update        Update "requirements*.txt" dependencies files                                                    │
│     update-readme-history                                                                                          │
│                   Update project history base on git commits/tags in README.md Will be exited with 1 if the        │
│                   README.md was updated otherwise with 0.                                                          │
│                                                                                                                    │
│                   Also, callable via e.g.:                                                                         │
│                       python -m cli_base update-readme-history -v                                                  │
│     update-test-snapshot-files                                                                                     │
│                   Update all test snapshot files (by remove and recreate all snapshot files)                       │
│     version       Print version and exit                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)


## History

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)



[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
