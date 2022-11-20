# cookiecutter templates

[![tests](https://github.com/jedie/cookiecutter_templates/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/cookiecutter_templates/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/cookiecutter_templates/branch/main/graph/badge.svg)](https://codecov.io/github/jedie/cookiecutter_templates)


## [Poetry Python Package](https://github.com/jedie/cookiecutter_templates/tree/main/poetry-python)

Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:

```shell
$ cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory poetry-python
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:

```shell
~/manageprojects$ ./mp.py start-project https://github.com/jedie/cookiecutter_templates/ --directory poetry-python ~/output/directory/
```



## [YunoHost Package for Django Apps](https://github.com/jedie/cookiecutter_templates/tree/main/yunohost_django_package)

Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:

```shell
$ cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory yunohost_django_package
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:

```shell
~/manageprojects$ ./mp.py start-project https://github.com/jedie/cookiecutter_templates/ --directory yunohost_django_package ~/output/directory/
```


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
