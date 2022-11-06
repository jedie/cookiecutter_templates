## local test

For quicker developing of {{cookiecutter.upstream_pkg_name}}_ynh in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone {{cookiecutter.upstream_url}}.git
~$ cd {{cookiecutter.upstream_pkg_name}}_ynh/
~/{{cookiecutter.upstream_pkg_name}}_ynh$ make
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

~/{{cookiecutter.upstream_pkg_name}}_ynh$ make install-poetry
~/{{cookiecutter.upstream_pkg_name}}_ynh$ make install
~/{{cookiecutter.upstream_pkg_name}}_ynh$ make local-test
```

Notes:

* SQlite database will be used
* A super user with username `test` and password `test` is created
* The page is available under `http://127.0.0.1:8000/app_path/`


## history




## Links

* Report a bug about this package: {{cookiecutter.upstream_url}}
* YunoHost website: https://yunohost.org/
* PyPi package: https://pypi.org/project/{{cookiecutter.upstream_pkg_name}}_ynh/

These projects used `{{cookiecutter.upstream_pkg_name}}_ynh`:

* {{cookiecutter.upstream_url}}

---

# Developer info

The App project will be stored under `__FINALPATH__` (e.g.: `/opt/yunohost/$app`) that's Django's `settings.FINALPATH`
"static" / "media" files to serve via nginx are under `__PUBLIC_PATH__` (e.g.: `/var/www/$app`) that's `settings.PUBLIC_PATH`

## package installation / debugging

This app is not in YunoHost app catalog. Test install, e.g.:
```bash
~# git clone {{cookiecutter.upstream_url}}.git
~# yunohost app install {{cookiecutter.upstream_pkg_name}}_ynh/ -f
```
To update:
```bash
~# cd {{cookiecutter.upstream_pkg_name}}_ynh
~/{{cookiecutter.upstream_pkg_name}}_ynh# git fetch && git reset --hard origin/testing
~/{{cookiecutter.upstream_pkg_name}}_ynh# yunohost app upgrade {{cookiecutter.upstream_pkg_name}}_ynh -u . -F
```

To remove call e.g.:
```bash
sudo yunohost app remove {{cookiecutter.upstream_pkg_name}}_ynh
```

Backup / remove / restore cycle, e.g.:
```bash
yunohost backup create --apps {{cookiecutter.upstream_pkg_name}}_ynh
yunohost backup list
archives:
  - {{cookiecutter.upstream_pkg_name}}_ynh-pre-upgrade1
  - 20201223-163434
yunohost app remove {{cookiecutter.upstream_pkg_name}}_ynh
yunohost backup restore 20201223-163434 --apps {{cookiecutter.upstream_pkg_name}}_ynh
```

Debug the installation, e.g.:
```bash
root@yunohost:~# cat /etc/yunohost/apps/{{cookiecutter.upstream_pkg_name}}_ynh/settings.yml
...

root@yunohost:~# ls -la /var/www/{{cookiecutter.upstream_pkg_name}}_ynh/
total 18
drwxr-xr-x 4 root root 4 Dec  8 08:36 .
drwxr-xr-x 6 root root 6 Dec  8 08:36 ..
drwxr-xr-x 2 root root 2 Dec  8 08:36 media
drwxr-xr-x 7 root root 8 Dec  8 08:40 static

root@yunohost:~# ls -la /opt/yunohost/{{cookiecutter.upstream_pkg_name}}_ynh/
total 58
drwxr-xr-x 5 {{cookiecutter.upstream_pkg_name}}_ynh {{cookiecutter.upstream_pkg_name}}_ynh   11 Dec  8 08:39 .
drwxr-xr-x 3 root        root           3 Dec  8 08:36 ..
-rw-r--r-- 1 {{cookiecutter.upstream_pkg_name}}_ynh {{cookiecutter.upstream_pkg_name}}_ynh  460 Dec  8 08:39 gunicorn.conf.py
-rw-r--r-- 1 {{cookiecutter.upstream_pkg_name}}_ynh {{cookiecutter.upstream_pkg_name}}_ynh    0 Dec  8 08:39 local_settings.py
-rwxr-xr-x 1 {{cookiecutter.upstream_pkg_name}}_ynh {{cookiecutter.upstream_pkg_name}}_ynh  274 Dec  8 08:39 manage.py
-rw-r--r-- 1 {{cookiecutter.upstream_pkg_name}}_ynh {{cookiecutter.upstream_pkg_name}}_ynh  171 Dec  8 08:39 secret.txt
drwxr-xr-x 6 {{cookiecutter.upstream_pkg_name}}_ynh {{cookiecutter.upstream_pkg_name}}_ynh    6 Dec  8 08:37 venv
-rw-r--r-- 1 {{cookiecutter.upstream_pkg_name}}_ynh {{cookiecutter.upstream_pkg_name}}_ynh  115 Dec  8 08:39 wsgi.py
-rw-r--r-- 1 {{cookiecutter.upstream_pkg_name}}_ynh {{cookiecutter.upstream_pkg_name}}_ynh 4737 Dec  8 08:39 {{cookiecutter.upstream_pkg_name}}_ynh_demo_settings.py

root@yunohost:~# cd /opt/yunohost/{{cookiecutter.upstream_pkg_name}}_ynh/
root@yunohost:/opt/yunohost/{{cookiecutter.upstream_pkg_name}}_ynh# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/{{cookiecutter.upstream_pkg_name}}_ynh# ./manage.py check
{{cookiecutter.upstream_pkg_name}}_ynh v0.8.2 (Django v2.2.17)
DJANGO_SETTINGS_MODULE='{{cookiecutter.upstream_pkg_name}}_ynh_demo_settings'
PROJECT_PATH:/opt/yunohost/{{cookiecutter.upstream_pkg_name}}_ynh/venv/lib/python3.7/site-packages
BASE_PATH:/opt/yunohost/{{cookiecutter.upstream_pkg_name}}_ynh
System check identified no issues (0 silenced).

root@yunohost:~# tail -f /var/log/{{cookiecutter.upstream_pkg_name}}_ynh/{{cookiecutter.upstream_pkg_name}}_ynh.log
root@yunohost:~# cat /etc/systemd/system/systemd.service
...

root@yunohost:~# systemctl reload-or-restart {{cookiecutter.upstream_pkg_name}}_ynh
root@yunohost:~# journalctl --unit={{cookiecutter.upstream_pkg_name}}_ynh --follow
```


