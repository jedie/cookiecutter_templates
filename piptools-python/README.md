# pip-tools based python package - CookieCutter template

* Requirement management with [pip-tools](https://github.com/jazzband/pip-tools):
  * Used `pip-compile` to freeze/pin requirements with hashes
  * Used `pip-sync` to install all needed packages
* [click](https://click.palletsprojects.com) based CLI for app and dev mode
* Auto virtualenv bootstrap, just by calling the `cli.py` / `dev-cli.py`
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Has basic unittest
