## local test

For quicker developing of {{cookiecutter.ynh_app_pkg_name}} in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone {{cookiecutter.upstream_url}}.git
~$ cd {{cookiecutter.ynh_app_pkg_name}}/
~/{{cookiecutter.ynh_app_pkg_name}}$ make
install-poetry         install or update poetry
install                install project via poetry
update                 update the sources and installation and generate "conf/requirements.txt"
lint                   Run code formatters and linter
fix-code-style         Fix code formatting
tox-listenvs           List all tox test environments
tox                    Run pytest via tox with all environments
pytest                 Run pytest
publish                Release new version to PyPi
local-test             Run local_test.py to run the project locally
local-diff-settings    Run "manage.py diffsettings" with local test

~/{{cookiecutter.ynh_app_pkg_name}}$ make install-poetry
~/{{cookiecutter.ynh_app_pkg_name}}$ make install
~/{{cookiecutter.ynh_app_pkg_name}}$ make local-test
```

Notes:

* SQlite database will be used
* A super user with username `test` and password `test` is created
* The page is available under `http://127.0.0.1:8000/app_path/`


## history




## Links

* Report a bug about this package: {{cookiecutter.upstream_url}}
* YunoHost website: https://yunohost.org/
* PyPi package: https://pypi.org/project/{{cookiecutter.ynh_app_pkg_name}}/

These projects used `{{cookiecutter.ynh_app_pkg_name}}`:

* {{cookiecutter.upstream_url}}

---

# Developer info

The App project will be stored under `__FINALPATH__` (e.g.: `/opt/yunohost/$app`) that's Django's `settings.FINALPATH`
"static" / "media" files to serve via nginx are under `__PUBLIC_PATH__` (e.g.: `/var/www/$app`) that's `settings.PUBLIC_PATH`

## package installation / debugging

This app is not in YunoHost app catalog. Test install, e.g.:
```bash
~# git clone {{cookiecutter.upstream_url}}.git
~# yunohost app install {{cookiecutter.ynh_app_pkg_name}}/ -f
```
To update:
```bash
~# cd {{cookiecutter.ynh_app_pkg_name}}
~/{{cookiecutter.ynh_app_pkg_name}}# git fetch && git reset --hard origin/testing
~/{{cookiecutter.ynh_app_pkg_name}}# yunohost app upgrade {{cookiecutter.ynh_app_pkg_name}} -u . -F
```

To remove call e.g.:
```bash
sudo yunohost app remove {{cookiecutter.ynh_app_pkg_name}}
```

Backup / remove / restore cycle, e.g.:
```bash
yunohost backup create --apps {{cookiecutter.ynh_app_pkg_name}}
yunohost backup list
archives:
  - {{cookiecutter.ynh_app_pkg_name}}-pre-upgrade1
  - 20201223-163434
yunohost app remove {{cookiecutter.ynh_app_pkg_name}}
yunohost backup restore 20201223-163434 --apps {{cookiecutter.ynh_app_pkg_name}}
```

Debug the installation, e.g.:
```bash
root@yunohost:~# cat /etc/yunohost/apps/{{cookiecutter.ynh_app_pkg_name}}/settings.yml
...

root@yunohost:~# ls -la /var/www/{{cookiecutter.ynh_app_pkg_name}}/
total 18
drwxr-xr-x 4 root root 4 Dec  8 08:36 .
drwxr-xr-x 6 root root 6 Dec  8 08:36 ..
drwxr-xr-x 2 root root 2 Dec  8 08:36 media
drwxr-xr-x 7 root root 8 Dec  8 08:40 static

root@yunohost:~# ls -la /opt/yunohost/{{cookiecutter.ynh_app_pkg_name}}/
total 58
drwxr-xr-x 5 {{cookiecutter.ynh_app_pkg_name}} {{cookiecutter.ynh_app_pkg_name}}   11 Dec  8 08:39 .
drwxr-xr-x 3 root        root           3 Dec  8 08:36 ..
-rw-r--r-- 1 {{cookiecutter.ynh_app_pkg_name}} {{cookiecutter.ynh_app_pkg_name}}  460 Dec  8 08:39 gunicorn.conf.py
-rw-r--r-- 1 {{cookiecutter.ynh_app_pkg_name}} {{cookiecutter.ynh_app_pkg_name}}    0 Dec  8 08:39 local_settings.py
-rwxr-xr-x 1 {{cookiecutter.ynh_app_pkg_name}} {{cookiecutter.ynh_app_pkg_name}}  274 Dec  8 08:39 manage.py
-rw-r--r-- 1 {{cookiecutter.ynh_app_pkg_name}} {{cookiecutter.ynh_app_pkg_name}}  171 Dec  8 08:39 secret.txt
drwxr-xr-x 6 {{cookiecutter.ynh_app_pkg_name}} {{cookiecutter.ynh_app_pkg_name}}    6 Dec  8 08:37 venv
-rw-r--r-- 1 {{cookiecutter.ynh_app_pkg_name}} {{cookiecutter.ynh_app_pkg_name}}  115 Dec  8 08:39 wsgi.py
-rw-r--r-- 1 {{cookiecutter.ynh_app_pkg_name}} {{cookiecutter.ynh_app_pkg_name}} 4737 Dec  8 08:39 {{cookiecutter.ynh_app_pkg_name}}_demo_settings.py

root@yunohost:~# cd /opt/yunohost/{{cookiecutter.ynh_app_pkg_name}}/
root@yunohost:/opt/yunohost/{{cookiecutter.ynh_app_pkg_name}}# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/{{cookiecutter.ynh_app_pkg_name}}# ./manage.py check
{{cookiecutter.ynh_app_pkg_name}} v0.8.2 (Django v2.2.17)
DJANGO_SETTINGS_MODULE='{{cookiecutter.ynh_app_pkg_name}}_demo_settings'
PROJECT_PATH:/opt/yunohost/{{cookiecutter.ynh_app_pkg_name}}/venv/lib/python3.7/site-packages
BASE_PATH:/opt/yunohost/{{cookiecutter.ynh_app_pkg_name}}
System check identified no issues (0 silenced).

root@yunohost:~# tail -f /var/log/{{cookiecutter.ynh_app_pkg_name}}/{{cookiecutter.ynh_app_pkg_name}}.log
root@yunohost:~# cat /etc/systemd/system/systemd.service
...

root@yunohost:~# systemctl reload-or-restart {{cookiecutter.ynh_app_pkg_name}}
root@yunohost:~# journalctl --unit={{cookiecutter.ynh_app_pkg_name}} --follow
```


