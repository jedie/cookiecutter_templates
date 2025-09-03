## Settings and upgrades

Almost everything related to {{ cookiecutter.project_name }}'s configuration is handled in a `"../conf/settings.py"` file.
You can edit the file `/home/yunohost.app/{{ cookiecutter.project_id }}/local_settings.py` to enable or disable features.

Test sending emails, e.g.:

```bash
ssh admin@yourdomain.tld
root@yunohost:~# /home/yunohost.app/{{ cookiecutter.project_id }}/manage.py sendtestemail --admins
```

How to debug a django YunoHost app, take a look into:

* {{ cookiecutter.ynh_app_url }}#developer-info

## local test

For quicker developing of {{ cookiecutter.ynh_app_pkg_name }} in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone https://github.com/YunoHost-Apps/{{ cookiecutter.project_id }}.git
~$ cd {{ cookiecutter.ynh_app_pkg_name }}/
~/{{ cookiecutter.project_id }}$ ./dev-cli.py --help
```


The output will looks like:

[comment]: <> (✂✂✂ auto generated help start ✂✂✂)
```
usage: ./dev-cli.py [-h]
                    {coverage,install,lint,mypy,nox,pip-audit,publish,test,update,update-test-snapshot-files,version}



╭─ options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ─────────────────────────────────────────────────────────────────────────────────────╮
│ {coverage,install,lint,mypy,nox,pip-audit,publish,test,update,update-test-snapshot-files,version} │
│     coverage      Run tests and show coverage report.                                             │
│     install       Install requirements and '{{ cookiecutter.ynh_app_pkg_name }}' via pip as editable.              │
│     lint          Check/fix code style by run: "ruff check --fix"                                 │
│     mypy          Run Mypy (configured in pyproject.toml)                                         │
│     nox           Run nox                                                                         │
│     pip-audit     Run pip-audit check against current requirements files                          │
│     publish       Build and upload this project to PyPi                                           │
│     test          Run unittests                                                                   │
│     update        Update "requirements*.txt" dependencies files                                   │
│     update-test-snapshot-files                                                                    │
│                   Update all test snapshot files (by remove and recreate all snapshot files)      │
│     version       Print version and exit                                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated help end ✂✂✂)
