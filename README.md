# cookiecutter templates

[![tests](https://github.com/jedie/cookiecutter_templates/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/cookiecutter_templates/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/cookiecutter_templates/branch/main/graph/badge.svg)](https://codecov.io/github/jedie/cookiecutter_templates)

All Templates are tested via unittests!

Patches welcome!

[comment]: <> (✂✂✂ auto generated start ✂✂✂)
## pipenv based python package

* Requirement management with [pipenv](https://pipenv.pypa.io)
* Makefile with a simple "help" menu
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Has basic unittest


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory pipenv-python
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory pipenv-python ~/foobar/
```

## pip-tools based python package

* Requirement management with [pip-tools](https://github.com/jazzband/pip-tools):
  * Used `pip-compile` to freeze/pin requirements with hashes
  * Used `pip-sync` to install all needed packages
* [Typer](https://typer.tiangolo.com/) based CLI
* Auto virtualenv bootstrap, just by calling the `cli.py`
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Has basic unittest


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory piptools-python
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory piptools-python ~/foobar/
```

## Poetry based python package

* Requirement management with [Poetry](https://python-poetry.org/)
* Bootstrap via `Makefile`
* [Typer](https://typer.tiangolo.com/) based CLI
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Has basic unittest


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory poetry-python
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory poetry-python ~/foobar/
```

## Base Django YunoHost app

[YunoHost](https://yunohost.org) is a Open-Source, Debian based self-hosting solution.

This CookieCutter template is useful to build a [YunoHost App](https://github.com/YunoHost-Apps/) for a [Django](https://docs.djangoproject.com) based Web application

* Contains all YunoHost scripts for install, backup, restore etc. action
* Used [django_yunohost_integration](https://github.com/YunoHost-Apps/django_yunohost_integration)
* Requirement management with [Poetry](https://python-poetry.org/)
* `Makefile` helper
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Project unittest with Django integration tests


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory yunohost_django_package
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory yunohost_django_package ~/foobar/
```
[comment]: <> (✂✂✂ auto generated end ✂✂✂)

# contribute

## setup local test enviorment

```bash
~$ git clone https://github.com/jedie/cookiecutter_templates.git
~$ cd cookiecutter_templates
~/cookiecutter_templates$ ./cli.py --help
...
 Usage: managetemplates [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.         │
│ --help                        Show this message and exit.                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ check-code-style                                                                                                       │
│ coverage                  Run and show coverage.                                                                       │
│ fix-code-style            Fix code style via darker                                                                    │
│ install                   Run pip-sync and install 'managetemplates' via pip as editable.                              │
│ mypy                      Run Mypy (configured in pyproject.toml)                                                      │
│ publish                   Build and upload this project to PyPi                                                        │
│ test                      Run unittests                                                                                │
│ update                    Update the development environment                                                           │
│ version                   Print version and exit                                                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Run tests, e.g.:
```bash
~/cookiecutter_templates$ ./cli.py test

# or sub tests:
~/cookiecutter_templates$ ./cli.py test managetemplates/tests/test_piptools_python.py

# It's just a "python3 -m unittest" wrapper cli, see:
~/cookiecutter_templates$ ./cli.py test --help
```


# Links

* https://github.com/jedie/manageprojects/
