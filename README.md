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


Cookiecutter template tests are here: [pipenv-python/tests.py](https://github.com/jedie/cookiecutter_templates/blob/main/pipenv-python/tests.py)


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


Cookiecutter template tests are here: [piptools-python/tests.py](https://github.com/jedie/cookiecutter_templates/blob/main/piptools-python/tests.py)


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory piptools-python
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory piptools-python ~/foobar/
```

## Poetry based reuseable Django app

* Requirement management with [Poetry](https://python-poetry.org/)
* Bootstrap via `Makefile`
* Makefile with a simple "help" menu
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Has basic unittest


Cookiecutter template tests are here: [poetry-django-app/tests.py](https://github.com/jedie/cookiecutter_templates/blob/main/poetry-django-app/tests.py)


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory poetry-django-app
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory poetry-django-app ~/foobar/
```

## Poetry based python package

* Requirement management with [Poetry](https://python-poetry.org/)
* Bootstrap via `Makefile`
* [Typer](https://typer.tiangolo.com/) based CLI
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Has basic unittest


Cookiecutter template tests are here: [poetry-python/tests.py](https://github.com/jedie/cookiecutter_templates/blob/main/poetry-python/tests.py)


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


Cookiecutter template tests are here: [yunohost_django_package/tests.py](https://github.com/jedie/cookiecutter_templates/blob/main/yunohost_django_package/tests.py)


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
```

The output of `./cli.py --help` looks like:

[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ check-code-style            Check code style by calling darker + flake8                          │
│ coverage                    Run and show coverage.                                               │
│ fix-code-style              Fix code style via darker                                            │
│ fix-file-content            Unify cookiecutter variables in file content. e.g.: "{{foo}}" -> "{{ │
│                             foo }}"                                                              │
│ fix-filesystem              Unify cookiecutter variables in the file/directory paths. e.g.:      │
│                             "/{{foo}}/{{bar}}.txt" -> "/{{ foo }}/{{ bar }}.txt"                 │
│ install                     Run pip-sync and install 'managetemplates' via pip as editable.      │
│ publish                     Build and upload this project to PyPi                                │
│ reverse                     Reverse a /.tests/<pkg_name>/ back to Cookiecutter template in:      │
│                             ./<pkg_name>/                                                        │
│ test                        Run unittests                                                        │
│ tox                         Run tox                                                              │
│ update                      Update the development environment                                   │
│ update-test-snapshot-files  Update all test snapshot files (by remove and recreate all snapshot  │
│                             files)                                                               │
│ version                     Print version and exit                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)

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
