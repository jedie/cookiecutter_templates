## local test

For quicker developing of django_example_ynh in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone https://github.com/john-doh/django_example.git
~$ cd django_example_ynh/
~/django_example_ynh$ make
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

~/django_example_ynh$ make install-poetry
~/django_example_ynh$ make install
~/django_example_ynh$ make local-test
```

Notes:

* SQlite database will be used
* A super user with username `test` and password `test` is created
* The page is available under `http://127.0.0.1:8000/app_path/`


## history




## Links

* Report a bug about this package: https://github.com/john-doh/django_example
* YunoHost website: https://yunohost.org/
* PyPi package: https://pypi.org/project/django_example_ynh/

These projects used `django_example_ynh`:

* https://github.com/john-doh/django_example

---

# Developer info

The App project will be stored under `__FINALPATH__` (e.g.: `/opt/yunohost/$app`) that's Django's `settings.FINALPATH`
"static" / "media" files to serve via nginx are under `__PUBLIC_PATH__` (e.g.: `/var/www/$app`) that's `settings.PUBLIC_PATH`

## package installation / debugging

This app is not in YunoHost app catalog. Test install, e.g.:
```bash
~# git clone https://github.com/john-doh/django_example.git
~# yunohost app install django_example_ynh/ -f
```
To update:
```bash
~# cd django_example_ynh
~/django_example_ynh# git fetch && git reset --hard origin/testing
~/django_example_ynh# yunohost app upgrade django_example_ynh -u . -F
```

To remove call e.g.:
```bash
sudo yunohost app remove django_example_ynh
```

Backup / remove / restore cycle, e.g.:
```bash
yunohost backup create --apps django_example_ynh
yunohost backup list
archives:
  - django_example_ynh-pre-upgrade1
  - 20201223-163434
yunohost app remove django_example_ynh
yunohost backup restore 20201223-163434 --apps django_example_ynh
```

Debug the installation, e.g.:
```bash
root@yunohost:~# cat /etc/yunohost/apps/django_example_ynh/settings.yml
...

root@yunohost:~# ls -la /var/www/django_example_ynh/
total 18
drwxr-xr-x 4 root root 4 Dec  8 08:36 .
drwxr-xr-x 6 root root 6 Dec  8 08:36 ..
drwxr-xr-x 2 root root 2 Dec  8 08:36 media
drwxr-xr-x 7 root root 8 Dec  8 08:40 static

root@yunohost:~# ls -la /opt/yunohost/django_example_ynh/
total 58
drwxr-xr-x 5 django_example_ynh django_example_ynh   11 Dec  8 08:39 .
drwxr-xr-x 3 root        root           3 Dec  8 08:36 ..
-rw-r--r-- 1 django_example_ynh django_example_ynh  460 Dec  8 08:39 gunicorn.conf.py
-rw-r--r-- 1 django_example_ynh django_example_ynh    0 Dec  8 08:39 local_settings.py
-rwxr-xr-x 1 django_example_ynh django_example_ynh  274 Dec  8 08:39 manage.py
-rw-r--r-- 1 django_example_ynh django_example_ynh  171 Dec  8 08:39 secret.txt
drwxr-xr-x 6 django_example_ynh django_example_ynh    6 Dec  8 08:37 venv
-rw-r--r-- 1 django_example_ynh django_example_ynh  115 Dec  8 08:39 wsgi.py
-rw-r--r-- 1 django_example_ynh django_example_ynh 4737 Dec  8 08:39 django_example_ynh_demo_settings.py

root@yunohost:~# cd /opt/yunohost/django_example_ynh/
root@yunohost:/opt/yunohost/django_example_ynh# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/django_example_ynh# ./manage.py check
django_example_ynh v0.8.2 (Django v2.2.17)
DJANGO_SETTINGS_MODULE='django_example_ynh_demo_settings'
PROJECT_PATH:/opt/yunohost/django_example_ynh/venv/lib/python3.7/site-packages
BASE_PATH:/opt/yunohost/django_example_ynh
System check identified no issues (0 silenced).

root@yunohost:~# tail -f /var/log/django_example_ynh/django_example_ynh.log
root@yunohost:~# cat /etc/systemd/system/systemd.service
...

root@yunohost:~# systemctl reload-or-restart django_example_ynh
root@yunohost:~# journalctl --unit=django_example_ynh --follow
```


