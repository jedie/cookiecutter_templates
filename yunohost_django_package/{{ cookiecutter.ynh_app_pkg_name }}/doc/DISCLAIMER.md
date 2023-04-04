## Settings and upgrades

Almost everything related to {{ cookiecutter.project_name }}'s configuration is handled in a `"../conf/settings.py"` file.
You can edit the file `/opt/yunohost/{{ cookiecutter.project_name }}/local_settings.py` to enable or disable features.

Test sending emails:

```bash
ssh admin@yourdomain.tld
root@yunohost:~# cd /opt/yunohost/{{ cookiecutter.project_name }}/
root@yunohost:/opt/yunohost/{{ cookiecutter.project_name }}# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/{{ cookiecutter.project_name }}# ./manage.py sendtestemail --admins
```

Background info: Error mails are send to all [settings.ADMINS](https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-ADMINS). By default the YunoHost admin is inserted here.
To check current ADMINS run:

```bash
(venv) root@yunohost:/opt/yunohost/{{ cookiecutter.project_name }}# ./manage.py sendtestemail --admins
```

If you prefere to send error emails to a extrnal email address, just do something like this:

```bash
echo "ADMINS = (('Your Name', 'example@domain.tld'),)" >> /opt/yunohost/{{ cookiecutter.project_name }}/local_settings.py
```

To check the effective settings, run this:
```bash
(venv) root@yunohost:/opt/yunohost/{{ cookiecutter.project_name }}# ./manage.py diffsettings
```


# Miscellaneous


## SSO authentication

[SSOwat](https://github.com/YunoHost/SSOwat) is fully supported via [django_ynh](https://github.com/YunoHost-Apps/django_ynh):

* First user (`$YNH_APP_ARG_ADMIN`) will be created as Django's super user
* All new users will be created as normal users
* Login via SSO is fully supported
* User Email, First / Last name will be updated from SSO data


## Links

 * Report a bug about this package: {{ cookiecutter.ynh_app_url }}
 * Report a bug about {{ cookiecutter.project_name }} itself: {{ cookiecutter.upstream_url }}
 * YunoHost website: https://yunohost.org/

---

# Developer info

## package installation / debugging

Please send your pull request to {{ cookiecutter.ynh_app_url }}

Try 'main' branch, e.g.:
```bash
sudo yunohost app install {{ cookiecutter.ynh_app_url }}/tree/master --debug
or
sudo yunohost app upgrade {{ cookiecutter.project_name }} -u {{ cookiecutter.ynh_app_url }}/tree/master --debug
```

Try 'testing' branch, e.g.:
```bash
sudo yunohost app install {{ cookiecutter.ynh_app_url }}/tree/testing --debug
or
sudo yunohost app upgrade {{ cookiecutter.project_name }} -u {{ cookiecutter.ynh_app_url }}/tree/testing --debug
```

To remove call e.g.:
```bash
sudo yunohost app remove {{ cookiecutter.project_name }}
```

Backup / remove / restore cycle, e.g.:
```bash
yunohost backup create --apps {{ cookiecutter.project_name }}
yunohost backup list
archives:
  - {{ cookiecutter.project_name }}-pre-upgrade1
  - 20201223-163434
yunohost app remove {{ cookiecutter.project_name }}
yunohost backup restore 20201223-163434 --apps {{ cookiecutter.project_name }}
```

Debug installation, e.g.:
```bash
root@yunohost:~# ls -la /var/www/{{ cookiecutter.project_name }}/
total 18
drwxr-xr-x 4 root root 4 Dec  8 08:36 .
drwxr-xr-x 6 root root 6 Dec  8 08:36 ..
drwxr-xr-x 2 root root 2 Dec  8 08:36 media
drwxr-xr-x 7 root root 8 Dec  8 08:40 static

root@yunohost:~# ls -la /opt/yunohost/{{ cookiecutter.project_name }}/
total 58
drwxr-xr-x 5 {{ cookiecutter.project_name }} {{ cookiecutter.project_name }}   11 Dec  8 08:39 .
drwxr-xr-x 3 root        root           3 Dec  8 08:36 ..
-rw-r--r-- 1 {{ cookiecutter.project_name }} {{ cookiecutter.project_name }}  460 Dec  8 08:39 gunicorn.conf.py
-rw-r--r-- 1 {{ cookiecutter.project_name }} {{ cookiecutter.project_name }}    0 Dec  8 08:39 local_settings.py
-rwxr-xr-x 1 {{ cookiecutter.project_name }} {{ cookiecutter.project_name }}  274 Dec  8 08:39 manage.py
-rw-r--r-- 1 {{ cookiecutter.project_name }} {{ cookiecutter.project_name }}  171 Dec  8 08:39 secret.txt
drwxr-xr-x 6 {{ cookiecutter.project_name }} {{ cookiecutter.project_name }}    6 Dec  8 08:37 venv
-rw-r--r-- 1 {{ cookiecutter.project_name }} {{ cookiecutter.project_name }}  115 Dec  8 08:39 wsgi.py
-rw-r--r-- 1 {{ cookiecutter.project_name }} {{ cookiecutter.project_name }} 4737 Dec  8 08:39 settings.py

root@yunohost:~# cd /opt/yunohost/{{ cookiecutter.project_name }}/
root@yunohost:/opt/yunohost/{{ cookiecutter.project_name }}# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/{{ cookiecutter.project_name }}# ./manage.py check
{{ cookiecutter.project_name }} v0.8.2 (Django v2.2.17)
DJANGO_SETTINGS_MODULE='settings'
PROJECT_PATH:/opt/yunohost/{{ cookiecutter.project_name }}/venv/lib/python3.7/site-packages
BASE_PATH:/opt/yunohost/{{ cookiecutter.project_name }}
System check identified no issues (0 silenced).

root@yunohost:~# tail -f /var/log/{{ cookiecutter.project_name }}/{{ cookiecutter.project_name }}.log
root@yunohost:~# cat /etc/systemd/system/{{ cookiecutter.project_name }}.service

root@yunohost:~# systemctl reload-or-restart {{ cookiecutter.project_name }}
root@yunohost:~# systemctl status {{ cookiecutter.project_name }}
root@yunohost:~# journalctl --unit={{ cookiecutter.upstream_pkg_app_name }} --follow
```

## local test

For quicker developing of {{ cookiecutter.project_name }} in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone {{ cookiecutter.ynh_app_url }}.git
~$ cd {{ cookiecutter.project_name }}_ynh/
~/{{ cookiecutter.project_name }}_ynh$ make
install-poetry         install or update poetry
install                install {{ cookiecutter.project_name }} via poetry
update                 update the sources and installation
local-test             Run local_test.py to run {{ cookiecutter.project_name }}_ynh locally
~/{{ cookiecutter.project_name }}_ynh$ make install-poetry
~/{{ cookiecutter.project_name }}_ynh$ make install
~/{{ cookiecutter.project_name }}_ynh$ make local-test
```

Notes:

* SQlite database will be used
* A super user with username `test` and password `test` is created
* The page is available under `http://127.0.0.1:8000/app_path/`
