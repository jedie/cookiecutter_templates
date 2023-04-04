# Django Project - CookieCutter template

* Requirement management with [pip-tools](https://github.com/jazzband/pip-tools):
  * Used `pip-compile` to freeze/pin requirements with hashes
  * Used `pip-sync` to install all needed packages
* [manage_django_project](https://github.com/jedie/manage_django_project):
  * Auto virtualenv bootstrap, just by calling the `manage.py`
  * Dev. managed commands
* used [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) for everything
