# uv based python package - CookieCutter template

* Requirement management with [uv](https://github.com/astral-sh/uv)
* [click](https://click.palletsprojects.com) based CLI for app and dev mode
* Auto virtualenv bootstrap, just by calling the `cli.py` / `dev-cli.py`
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
* Base requirements are only: `python3-venv` and `python3-pip` (uv will ne installed via pip in `.venv`)
* Has basic unittest
