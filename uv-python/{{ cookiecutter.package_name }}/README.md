# {{ cookiecutter.project_name }}

[![tests]({{ cookiecutter.package_url }}/actions/workflows/tests.yml/badge.svg?branch=main)]({{ cookiecutter.package_url }}/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}/branch/main/graph/badge.svg)](https://app.codecov.io/github/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }})
[![{{ cookiecutter.package_name }} @ PyPi](https://img.shields.io/pypi/v/{{ cookiecutter.package_name }}?label={{ cookiecutter.package_name }}%20%40%20PyPi)](https://pypi.org/project/{{ cookiecutter.package_name }}/)
[![Python Versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.package_name }})]({{ cookiecutter.package_url }}/blob/main/pyproject.toml)
[![License {{ cookiecutter.license }}](https://img.shields.io/pypi/l/{{ cookiecutter.package_name }})]({{ cookiecutter.package_url }}/blob/main/LICENSE)

{{ cookiecutter.package_description }}

## Usage

### preperation

Note: If you using a Raspberry Pi: Check that https://www.piwheels.org/ are in use.
For this, just look into `etc/pip.conf` it should be looked like this:
```bash
~/pysmartmeter$ cat /etc/pip.conf
[global]
extra-index-url=https://www.piwheels.org/simple
```

### Installation

The easiest way is to install "{{ cookiecutter.project_name }}" via [pipx](https://pipx.pypa.io/), e.g.:
```bash
~$ sudo apt install pipx
~$ pipx install --verbose {{ cookiecutter.project_name }}
```
Then just call `{{ cookiecutter.project_name }}` CLI, e.g.:
```bash
~$ {{ cookiecutter.project_name }} --help
```

[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
usage: {{ cookiecutter.project_name }} [-h] {shell-completion,version}



╭─ options ─────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help            show this help message and exit                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ─────────────────────────────────────────────────────────────────────────────╮
│ (required)                                                                                │
│   • shell-completion  Setup shell completion for this CLI (Currently only for bash shell) │
│   • version           Print version and exit                                              │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)


## start development

At least `uv` is needed. Install e.g.: via pipx:
```bash
apt-get install pipx
pipx install uv
```

Clone the project and just start the CLI help commands.
A virtual environment will be created/updated automatically.

```bash
~$ git clone {{ cookiecutter.package_url }}.git
~$ cd {{ cookiecutter.package_name }}
~/{{ cookiecutter.package_name }}$ ./cli.py --help
~/{{ cookiecutter.package_name }}$ ./dev-cli.py --help
```

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
usage: ./dev-cli.py [-h] {coverage,install,lint,mypy,nox,pip-audit,publish,shell-completion,test,update,update-readme-history,update-test-snapshot-files,version}



╭─ options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help     show this help message and exit                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ (required)                                                                                                           │
│   • coverage   Run tests and show coverage report.                                                                   │
│   • install    Install requirements and '{{ cookiecutter.package_name }}' via pip as editable.                                     │
│   • lint       Check/fix code style by run: "ruff check --fix"                                                       │
│   • mypy       Run Mypy (configured in pyproject.toml)                                                               │
│   • nox        Run nox                                                                                               │
│   • pip-audit  Run pip-audit check against current requirements files                                                │
│   • publish    Build and upload this project to PyPi                                                                 │
│   • shell-completion                                                                                                 │
│                Setup shell completion for this CLI (Currently only for bash shell)                                   │
│   • test       Run unittests                                                                                         │
│   • update     Update dependencies (uv.lock) and git pre-commit hooks                                                │
│   • update-readme-history                                                                                            │
│                Update project history base on git commits/tags in README.md Will be exited with 1 if the README.md   │
│                was updated otherwise with 0.                                                                         │
│                                                                                                                      │
│                Also, callable via e.g.:                                                                              │
│                    python -m cli_base update-readme-history -v                                                       │
│   • update-test-snapshot-files                                                                                       │
│                Update all test snapshot files (by remove and recreate all snapshot files)                            │
│   • version    Print version and exit                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)


## History

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)



[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
