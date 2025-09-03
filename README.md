# cookiecutter templates

[![tests](https://github.com/jedie/cookiecutter_templates/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/cookiecutter_templates/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/cookiecutter_templates/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/cookiecutter_templates)

All Templates are tested via unittests!

Patches welcome!

[comment]: <> (✂✂✂ auto generated start ✂✂✂)
## uv based python package with a Makefile

* Requirement management with [uv](https://github.com/astral-sh/uv)
* Makefile with a simple "help" menu
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Base requirements are only: `python3-venv` and `python3-pip` (uv will ne installed via pip in `.venv`)
* Has basic unittest


Cookiecutter template tests are here: [make-uv-python/tests.py](https://github.com/jedie/cookiecutter_templates/blob/main/make-uv-python/tests.py)


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory make-uv-python
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory make-uv-python ~/foobar/
```

## Django Project

* Requirement management with [pip-tools](https://github.com/jazzband/pip-tools):
  * Used `pip-compile` to freeze/pin requirements with hashes
  * Used `pip-sync` to install all needed packages
* [manage_django_project](https://github.com/jedie/manage_django_project):
  * Auto virtualenv bootstrap, just by calling the `manage.py`
  * Dev. managed commands
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything


Cookiecutter template tests are here: [managed-django-project/tests.py](https://github.com/jedie/cookiecutter_templates/blob/main/managed-django-project/tests.py)


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory managed-django-project
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory managed-django-project ~/foobar/
```

## uv based python package

* Requirement management with [uv](https://github.com/astral-sh/uv)
* [click](https://click.palletsprojects.com) based CLI for app and dev mode
* Auto virtualenv bootstrap, just by calling the `cli.py` / `dev-cli.py`
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Base requirements are only: `python3-venv` and `python3-pip` (uv will ne installed via pip in `.venv`)
* Has basic unittest


Cookiecutter template tests are here: [uv-python/tests.py](https://github.com/jedie/cookiecutter_templates/blob/main/uv-python/tests.py)


Use with vanilla [cookiecutter](https://github.com/cookiecutter/cookiecutter), e.g.:
```shell
cookiecutter https://github.com/jedie/cookiecutter_templates/ --directory uv-python
```

Use with [manageprojects](https://github.com/jedie/manageprojects), e.g.:
```shell
./cli.py start-project https://github.com/jedie/cookiecutter_templates/ --directory uv-python ~/foobar/
```

## Base Django YunoHost app

[YunoHost](https://yunohost.org) is a Open-Source, Debian based self-hosting solution.

This CookieCutter template is useful to build a [YunoHost App](https://github.com/YunoHost-Apps/) for a [Django](https://docs.djangoproject.com) based Web application

* Contains all YunoHost scripts for install, backup, restore etc. action
* Used [django_yunohost_integration](https://github.com/YunoHost-Apps/django_yunohost_integration)
* Requirement management with [pip-tools](https://github.com/jazzband/pip-tools)
* [click](https://click.palletsprojects.com) based CLI
* Auto virtualenv bootstrap, just by calling `dev-cli.py`
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
usage: ./cli.py [-h] {fix-file-content,fix-filesystem,reverse,templates2generated,update-template-req,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ {fix-file-content,fix-filesystem,reverse,templates2generated,update-template-req,version}                          │
│     fix-file-content                                                                                               │
│                   Unify cookiecutter variables in file content. e.g.: "{{foo}}" -> "{{ foo }}"                     │
│     fix-filesystem                                                                                                 │
│                   Unify cookiecutter variables in the file/directory paths. e.g.: "/{{foo}}/{{bar}}.txt" -> "/{{   │
│                   foo }}/{{ bar }}.txt"                                                                            │
│     reverse       Reverse a /generated_templates/<pkg_name>/ back to Cookiecutter template in: ./<pkg_name>/ Note: │
│                   The reversed cookiecutter template files cannot be accepted 1-to-1.                              │
│     templates2generated                                                                                            │
│                   Generate all cookiecutter templates                                                              │
│     update-template-req                                                                                            │
│                   Update requirements of all cookiecutter templates                                                │
│     version       Print version and exit                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
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


# The dev. CLI

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
usage: ./dev-cli.py [-h]
                    {coverage,install,lint,mypy,nox,pip-audit,publish,test,update,update-readme-history,update-test-sn
apshot-files,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ {coverage,install,lint,mypy,nox,pip-audit,publish,test,update,update-readme-history,update-test-snapshot-files,ver │
│ sion}                                                                                                              │
│     coverage      Run tests and show coverage.                                                                     │
│     install       Install requirements and 'managetemplates' via pip as editable.                                  │
│     lint          Check/fix code style by run: "ruff check --fix"                                                  │
│     mypy          Run Mypy (configured in pyproject.toml)                                                          │
│     nox           Run nox                                                                                          │
│     pip-audit     Run pip-audit check against current requirements files                                           │
│     publish       Build and upload this project to PyPi                                                            │
│     test          Run unittests                                                                                    │
│     update        Update dependencies (uv.lock) and git pre-commit hooks                                           │
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


# History

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [**dev**](https://github.com/jedie/cookiecutter_templates/compare/v0.9.0...main)
  * 2025-09-03 - fix uv-python tests
  * 2025-09-03 - fix yunohost_django_package tests
  * 2025-09-03 - Bugfix coverage collecting
  * 2025-09-03 - fix ruff doc link for isort settings
  * 2025-09-03 - Enforce file permissions via tests
  * 2025-09-03 - fix README test
  * 2025-09-03 - fix templates
  * 2025-09-03 - add missing rich.print import
  * 2025-09-03 - managed-django-project: Replace Darker with ruff
  * 2025-09-03 - yunohost_django_package: Replace Draker with ruff
  * 2025-09-03 - fix code style
  * 2025-09-03 - Use assert_code_style() in CLI
  * 2025-09-03 - Replace darker with ruff
  * 2025-09-03 - make-uv-python: Replace darker with ruff
  * 2025-09-03 - uv-python:_replace darker with ruff
* [v0.9.0](https://github.com/jedie/cookiecutter_templates/compare/v0.3.0...v0.9.0)
  * 2025-08-05 - less test output
  * 2025-08-05 - Update managetemplates e.g.: click -> tyro
  * 2025-08-05 - update precommit in manage-django-project
  * 2025-08-05 - Update make-uv-python requirements
  * 2025-08-05 - Update managed-django-project requirements
  * 2025-08-05 - update uv-python requirements
  * 2025-08-05 - Update requirements
  * 2025-08-05 - Update nox in Django projects and use: DJANGO_VERSIONS = ['5.2', '5.1', '4.2']
  * 2025-08-05 - Bugfix nox config to install the correct Django version
  * 2025-06-10 - Cleanup README
  * 2025-06-10 - Remove pipenv and piptools templates
  * 2025-06-10 - split PHONY
  * 2025-06-10 - make-uv-python: tox -> nox + setuptools -> hatchling
  * 2025-06-02 - manage-django-project: Bugfix coverage run and DB transaction errors in tests
  * 2025-05-01 - managed-django-project: replace setuptools with hatchling
  * 2025-04-22 - bugfix hatch packages list
  * 2025-04-22 - replace setuptools with hatchling
  * 2025-04-22 - uv-python: Move readme command into dev-app
  * 2025-03-23 - Yunohost: update requirements
  * 2025-03-23 - Yunohost package: Bugfix upgrade script
  * 2025-03-23 - Bugfix double unitttest setup
  * 2025-03-23 - Remove unused imports
  * 2025-03-23 - Update pre-commit versions
  * 2025-03-23 - Remove warnings around cm.invoke() usage
  * 2025-03-23 - Update test snapshot
  * 2025-03-23 - Bugfix test call
  * 2025-03-23 - Remove rich_traceback_install() (It seems to be not very helpfull)
  * 2025-03-23 - YunoHost app simplify/enhance logging
  * 2025-03-21 - Update template requirements
  * 2025-03-21 - Yunohost template: Migrate "pip-tools" to "uv" and "click" to "tyro"
  * 2025-02-12 - uv-python: tox -> nox
  * 2025-02-12 - Update managed-django-project template
  * 2025-01-11 - set yunohost = ">=12"
  * 2024-12-23 - Update YunoHost template
  * 2024-12-03 - Use new cli_base
  * 2024-12-03 - Remove tyro work-a-round
  * 2024-11-21 - Replace click by tyro in uv-python
  * 2024-11-14 - New template: "make-uv-python"
  * 2024-11-13 - Migrate to uv
  * 2024-11-13 - Bugfix uv-python
  * 2024-10-29 - Add "uv-python" template
  * 2024-09-26 - Move pip-compile settings into pyproject.toml + create pywheel hashes
  * 2024-09-26 - Add "setup Python" to YunoHost template
  * 2024-09-25 - Simplify: Use update_readme_history() from cli-base-utilities
  * 2024-09-25 - Bugfix github CI matrix: "3.13" is only available via RC... Skip it until release.
  * 2024-09-25 - Apply own project updates from own template ;)
  * 2024-09-25 - Bugfix "pre-commit" call
  * 2024-09-25 - Updates for "piptools-python" template:
  * 2024-09-22 - Move pip-compile settings into pyproject.toml and add piwheels hashes
  * 2024-09-09 - Update YunoHost package: reuse existing venv and use pip-sync
  * 2024-09-05 - update manage-django-project
  * 2024-09-05 - Update template requirements and some min. Python specification
  * 2024-09-05 - "bin/python" -> "bin/python3"
  * 2024-09-05 - Enhance output and use EncloseRuleContext or Rule
  * 2024-08-30 - Add docstring link to "version-specifiers"
  * 2024-08-30 - CLIs: catch KeyboardInterrupt
  * 2024-08-30 - Update yunohost_django_package
  * 2024-08-25 - Update yunohost_django_package from https://github.com/YunoHost-Apps/django-for-runners_ynh
  * 2024-08-25 - Use typeguard in tests
  * 2024-08-25 - Use always "python3" instead of "python"
  * 2024-08-25 - Work-a-round for: https://github.com/jazzband/pip-tools/issues/1866
  * 2024-08-25 - Remove poetry based templates!
  * 2024-08-25 - Update requirements + CI config + test matrix
  * 2024-08-02 - Finalize replace "safety" by "pip-audit
  * 2024-08-02 - Replace safety with pip-audit
  * 2024-07-16 - Always pip and pip-tools if updates are needed
  * 2024-07-09 - pipenv-python: Move requirements into pyproject.toml
  * 2024-07-08 - Update pipenv-python template
  * 2024-05-21 - Ignore safety #67599
  * 2024-03-12 - Split CLI
  * 2024-03-12 - piptools-python: Split CLI into app/dev CLI packages
  * 2024-03-12 - Use @cli.command()
  * 2024-02-29 - remove obsolete darker options + update requirements
  * 2024-01-16 - Move typeguard install_import_hook
  * 2024-01-16 - piptools-python: Add typeguard
  * 2023-12-29 - piptools-python: Still support Python v3.9
  * 2023-12-22 - -MAP_DOWNLOAD
  * 2023-12-22 - +[*.{html,css,js}]
  * 2023-12-22 - Exclude "dist" directory
  * 2023-12-22 - Update managed-django-project
* [v0.3.0](https://github.com/jedie/cookiecutter_templates/compare/e968ed9...v0.3.0)
  * 2023-12-21 - Update manageprojects updates
  * 2023-12-21 - gitignore: +/build/
  * 2023-12-21 - Unify BASE_PATH / PACKAGE_ROOT etc.
  * 2023-12-21 - fix darker + Django v5.0 + Python >=3.10
  * 2023-12-21 - managed-django-project fix missing placeholders
  * 2023-12-21 - managed-django-project: Min. Python v3.10
  * 2023-12-21 - {{ cookiecutter.package_name }}_project -> {{ cookiecutter.django_project_name }}
  * 2023-12-03 - yunohost_django_package: project setup updates
  * 2023-12-03 - yunohost_django_package: Update requirements
  * 2023-12-17 - Update django test matrix: Add v5.0 and remove v4.1
  * 2023-12-17 - Copy all requirements files back
  * 2023-12-17 - Bugfix CI: Checkout all for darker
  * 2023-12-17 - Github CI: Include all requirements files into cache dependency
  * 2023-12-17 - Github CI: Display warnings only for test run step
  * 2023-12-17 - Configure unittests via "load_tests Protocol"
  * 2023-12-17 - Update requirements
  * 2023-12-17 - remove unused .../tests/utils.py file
  * 2023-12-17 - Django projects: AUTOLOGIN in local env as default
  * 2023-12-16 - editorconfig: Add "*.yaml"
  * 2023-12-02 - Use tools from cli_base
  * 2023-12-01 - Bugfix local tox run
  * 2023-12-01 - Update piptools-python template
  * 2023-11-30 - WIP: piptools-python updates
  * 2023-11-30 - DjangoYnhTestCase better error messages
  * 2023-11-30 - update requirements and add "flake8-bugbear"
  * 2023-11-28 - django prijects: cleanup settings
  * 2023-11-26 - Cleanup YunoHost app tests
  * 2023-11-26 - Yunohost Package: Remove pytest and use normal unittests
  * 2023-11-25 - __DEBUG_ENABLED__ "YES" / "NO" -> "1" / "0"
  * 2023-11-25 - Update generated yunohost template
  * 2023-11-25 - ynh package: debug_enabled: type = "boolean"
  * 2023-11-25 - ynh package: Comment "website" link.
  * 2023-11-25 - ynh package: doc/{DISCLAIMER.md => ADMIN.md}
  * 2023-11-25 - Small updates
  * 2023-11-25 - YunoHost package: Nicer Links in README to CI services
  * 2023-11-09 - fix yunohost_django_package snapshot test
  * 2023-11-09 - Update and run yunohost_django_package/update_requirements.py
  * 2023-11-09 - Update template requirements
  * 2023-11-09 - Add beautifulsoup4 because of html snapshot test
  * 2023-11-09 - Fix version check
  * 2023-11-09 - Update generated_templates/yunohost_django_package
  * 2023-11-09 - YunoHost Template: Add "config_panel.toml" with work-a-round.
  * 2023-11-09 - Add indirect depencies as work-a-round
  * 2023-11-09 - YunoHost template: pytest: disable_warnings = ["couldnt-parse"]
  * 2023-11-09 - YunoHost template: Check github only if version checks passed before
  * 2023-11-09 - YunoHost template: Snapshot the page
  * 2023-11-09 - YunoHost template: fix CI
  * 2023-11-09 - fix yunohost template
  * 2023-11-01 - Yunohost Django Package cleanup "poetry -> pip-tools" migration
  * 2023-11-01 - Yunohost Django package: Replace Poetry with pip-tools
  * 2023-11-01 - git ignore: +*.orig
  * 2023-10-08 - Bugfix pipenv template (darker extras)
  * 2023-10-08 - Add Python v3.12
  * 2023-08-22 - Update YunoHost test for new manifest v2 file
  * 2023-08-22 - Remove obsolete YunoHost config files
  * 2023-08-21 - Update YunoHost Django Package template to "Manifest v2"
  * 2023-08-22 - Update poetry-django-app
  * 2023-08-22 - +/coverage.*
  * 2023-08-17 - Don't exist cmd2 shell on "Interrupt from keyboard"
  * 2023-08-17 - Use argument to call the CLI entry point
  * 2023-08-17 - Bugfix Python 3.9 compatibility
  * 2023-08-17 - Migrate to cli_base.cli_tools.git and cli_base.cli_tools.version_info
  * 2023-08-17 - Bugfix yunohost_django_package
  * 2023-08-17 - Use cli-base-utilities and template updates and bugfixes
  * 2023-08-05 - split CLI
  * 2023-08-05 - Bugfix github actions for piptools-python
  * 2023-06-11 - update requirements and fix "tomli"
  * 2023-05-07 - Split piptols-python cli: "cli.py" and "dev-cli.py"
  * 2023-04-13 - Refactor yunohost_django_package context
  * 2023-04-10 - Add "project_name" to managed-django-project template
  * 2023-04-10 - remove snapshot test ;)
  * 2023-04-10 - Update requirements in templates
  * 2023-04-10 - use the real URl to https://github.com/jedie/django_example
  * 2023-04-10 - Update django_example.__version__ in yunohost_django_package/cookiecutter.json
  * 2023-04-10 - Dev
  * 2023-04-10 - templates2generated: force recreate as default
  * 2023-04-10 - Enhance managed-django-project
  * 2023-04-10 - Hacky way to expand the failed test output
  * 2023-04-10 - +license = "{{ cookiecutter.license }}" (#60)
  * 2023-04-07 - +license = "{{ cookiecutter.license }}"
  * 2023-04-06 - WIP:  add generated template into repository
  * 2023-04-05 - Udpate managed-django-project to manage_django_project v0.3.0
  * 2023-04-04 - NEW: "managed-django-project" template
  * 2023-04-04 - Update yunohost_django_package template
  * 2023-04-02 - Add setuptools_scm to include all files from git repository
  * 2023-04-02 - fix poetry-python
  * 2023-04-02 - Fix darker/flynt/isort/Pygments combination
  * 2023-03-17 - Update templates
  * 2023-03-17 - Use: dynamic = ["version"]
  * 2023-03-07 - Run DocTests via helper from bx_py_utils
  * 2023-03-06 - Coverage2
  * 2023-03-06 - Bugfix link to codecov.io
  * 2023-03-06 - Py 3.11 tomllib vs. tomli
  * 2023-03-06 - Updates
  * 2023-03-06 - unify github action configs
  * 2023-03-06 - fix coverage setup
  * 2023-02-20 - Tox
  * 2023-02-19 - replace "coveralls" with "coverage"
  * 2023-02-19 - piptools-python: Replace typer CLI with click and add flynt to darker
  * 2023-02-19 - Update via manageprojects
  * 2023-02-18 - add "make install-base-req" target to install needed OS base packages
  * 2023-02-07 - Update .flake8
  * 2023-02-07 - Cleanup Makefiles
  * 2023-02-07 - Update pythonapp.yml
  * 2023-02-07 - Add a reuseable Django App
  * 2023-02-05 - Bugfix cli and tests
  * 2023-02-05 - Bugfix publish test
  * 2023-02-05 - Bugfix tests and capture logs
  * 2023-02-05 - Bugfix excludes
  * 2023-02-05 - Change CLI from typer to click
  * 2023-02-05 - fix code style
  * 2023-02-05 - Apply "fix-file-content"
  * 2023-02-05 - Add "fix-file-content" CLI command to unify Cookiecutter vars in file contents
  * 2023-02-05 - fix tests
  * 2023-02-05 - Force unique var syntax in filesystem path by unittest
  * 2023-02-05 - Apply "fix-filesystem"
  * 2023-02-05 - Add "fix-filesystem" CLI command to rename e.g.: "/{{foo}}/{{bar}}.txt" -> "/{{ foo }}/{{ bar }}.txt"
  * 2023-01-13 - Fix github actions
  * 2023-01-13 - Move test files to the templates
  * 2023-01-13 - poetry-python: Refactor tox setup
  * 2023-01-12 - Update DocString, too.
  * 2023-01-12 - "http://" -> "https://"
  * 2023-01-12 - piptools-python: rename extras from "tests" to "dev"
  * 2023-01-11 - Don't check Github version while running in GitHub actions
  * 2023-01-10 - Update piptools-python and code style fix+lint
  * 2023-01-10 - Bugfix poetry-python template
  * 2023-01-10 - NEW: Reverse a /.tests/<pkg_name>/ back to Cookiecutter template in: ./<pkg_name>/
  * 2023-01-10 - Enhance CLI and code style linting + fixing
  * 2023-01-10 - constants.TEST_PATH
  * 2023-01-10 - Remove "[tool.flake8]" because it's unsupported, yet.
  * 2023-01-10 - Enhance poetry-python template
  * 2023-01-10 - Use constants.ALL_TEMPLATES
  * 2023-01-10 - Test if dir exists
  * 2023-01-09 - Use a more relaxed flak8 exclude rule
  * 2023-01-08 - Doc strings: fix github link to darker project
  * 2022-12-30 - Refactor "dependencies" definition
  * 2022-12-30 - [tool.setuptools] -> include all packages
  * 2022-12-30 - poetry-python: Use rich print and add "version" command
  * 2022-12-30 - set max line length to 119
  * 2022-12-30 - pipenv-python: add .flake8
  * 2022-12-30 - fix gitignore
  * 2022-12-30 - .editorconfig *.yml == indent_size = 2
  * 2022-12-30 - Nicer Typer init
  * 2022-12-30 - Enhance default test run and piptools-python project
  * 2022-12-30 - Delete coverage.json
  * 2022-12-21 - Update test_project_setup.py
  * 2022-12-21 - Update settings.py
  * 2022-12-21 - Update pyproject.toml
  * 2022-12-21 - borrow package linter from homeassistant_ynh
  * 2022-12-21 - yunohost_django_package: Check code style in tests
  * 2022-12-21 - yunohost_django_package: remove pytest-darker
  * 2022-12-21 - yunohost_django_package: Add "3.11" to test matrix
  * 2022-12-21 - piptools-python: Use new pip-compile resolver
  * 2022-11-30 - Expand test timeouts
  * 2022-11-30 - Add "dynamic" README with all existing templates
  * 2022-11-21 - Fix "yunohost_django_package" tests
  * 2022-11-21 - Bugfix "yunohost_django_package" code style
  * 2022-11-21 - Bugfix "yunohost_django_package" context
  * 2022-11-21 - Add work-a-round for "poetry install" bug
  * 2022-11-20 - Work-a-round for https://github.com/jazzband/pip-tools/issues/994#issuecomment-1321226661
  * 2022-11-20 - Enhance Github CI config
  * 2022-11-20 - +[tool.coverage.report]
  * 2022-11-20 - isort "skip_glob": add ".*"
  * 2022-11-20 - +pip-tools
  * 2022-11-20 - Update pip first
  * 2022-11-20 - update READMEs
  * 2022-11-20 - Update README.md
  * 2022-11-20 - fix darker
  * 2022-11-20 - Compile "piptools-python" requirements on "update" command, too.
  * 2022-11-20 - Use Git and subprocess_utils from manageprojects
  * 2022-11-20 - install() after update is not needed, because the bootstrap will does this.
  * 2022-11-20 - More tests for cli
  * 2022-11-20 - applied migrations "68124d4"
  * 2022-11-19 - fix github action
  * 2022-11-19 - remove unused file
  * 2022-11-19 - Add github CI file to "piptools-python" template
  * 2022-11-19 - Switch from poetry to piptool template
  * 2022-11-19 - Delete .coverage
  * 2022-11-19 - Add CLI to piptools-python template and add basic tests
  * 2022-11-19 - rename "minimal-python" to "piptools-python"
  * 2022-11-19 - fix isort + flake8
  * 2022-11-19 - Template + test updates
  * 2022-11-15 - Bugfix missing new Version
  * 2022-11-15 - Bugfix wrong CI workflow file
  * 2022-11-15 - Start testing
  * 2022-11-15 - start adding tests
  * 2022-11-14 - fix flake8 call
  * 2022-11-14 - +tomli
  * 2022-11-14 - bugfix and expand "poetry-python" template
  * 2022-11-14 - fix template
  * 2022-11-14 - Add a cli and CI setup
  * 2022-11-13 - Work-a-round for https://github.com/pypa/setuptools/issues/3278
  * 2022-11-13 - bugfix poetry template
  * 2022-11-13 - Add poetry-python template
  * 2022-11-13 - use importlib.metadata.version
  * 2022-11-10 - add a pipenv-python template
  * 2022-11-10 - fix make update-requirements
  * 2022-11-10 - remove pytest
  * 2022-11-10 - add minimal-python
  * 2022-11-10 - Bugfix: Create PEP 440 version
  * 2022-11-06 - "{{cookiecutter.author_name}}" -> "{{cookiecutter.full_name}}"
  * 2022-11-06 - {{cookiecutter.upstream_pkg_name}}_ynh -> {{cookiecutter.ynh_app_pkg_name}}
  * 2022-11-06 - -upstream_name +upstream_pkg_name
  * 2022-11-06 - remove lock file
  * 2022-11-06 - Bugfix unable to create file '.github/workflows/pytest.yml'
  * 2022-11-06 - Add yunohost_django_package
  * 2022-11-04 - Initial commit

[comment]: <> (✂✂✂ auto generated history end ✂✂✂)


# Links

* https://github.com/jedie/manageprojects/
