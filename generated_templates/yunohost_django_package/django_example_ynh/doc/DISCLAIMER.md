## Settings and upgrades

Almost everything related to Django Example's configuration is handled in a `"../conf/settings.py"` file.
You can edit the file `/opt/yunohost/Django Example/local_settings.py` to enable or disable features.

Test sending emails:

```bash
ssh admin@yourdomain.tld
root@yunohost:~# cd /opt/yunohost/Django Example/
root@yunohost:/opt/yunohost/Django Example# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/Django Example# ./manage.py sendtestemail --admins
```

Background info: Error mails are send to all [settings.ADMINS](https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-ADMINS). By default the YunoHost admin is inserted here.
To check current ADMINS run:

```bash
(venv) root@yunohost:/opt/yunohost/Django Example# ./manage.py sendtestemail --admins
```

If you prefere to send error emails to a extrnal email address, just do something like this:

```bash
echo "ADMINS = (('Your Name', 'example@domain.tld'),)" >> /opt/yunohost/Django Example/local_settings.py
```

To check the effective settings, run this:
```bash
(venv) root@yunohost:/opt/yunohost/Django Example# ./manage.py diffsettings
```


# Miscellaneous


## SSO authentication

[SSOwat](https://github.com/YunoHost/SSOwat) is fully supported via [django_ynh](https://github.com/YunoHost-Apps/django_ynh):

* First user (`$YNH_APP_ARG_ADMIN`) will be created as Django's super user
* All new users will be created as normal users
* Login via SSO is fully supported
* User Email, First / Last name will be updated from SSO data


## Links

 * Report a bug about this package: https://github.com/YunoHost-Apps/django_example_ynh
 * Report a bug about Django Example itself: https://github.com/john-doh/django_example
 * YunoHost website: https://yunohost.org/

---

# Developer info

## package installation / debugging

Please send your pull request to https://github.com/YunoHost-Apps/django_example_ynh

Try 'main' branch, e.g.:
```bash
sudo yunohost app install https://github.com/YunoHost-Apps/django_example_ynh/tree/master --debug
or
sudo yunohost app upgrade Django Example -u https://github.com/YunoHost-Apps/django_example_ynh/tree/master --debug
```

Try 'testing' branch, e.g.:
```bash
sudo yunohost app install https://github.com/YunoHost-Apps/django_example_ynh/tree/testing --debug
or
sudo yunohost app upgrade Django Example -u https://github.com/YunoHost-Apps/django_example_ynh/tree/testing --debug
```

To remove call e.g.:
```bash
sudo yunohost app remove Django Example
```

Backup / remove / restore cycle, e.g.:
```bash
yunohost backup create --apps Django Example
yunohost backup list
archives:
  - Django Example-pre-upgrade1
  - 20201223-163434
yunohost app remove Django Example
yunohost backup restore 20201223-163434 --apps Django Example
```

Debug installation, e.g.:
```bash
root@yunohost:~# ls -la /var/www/Django Example/
total 18
drwxr-xr-x 4 root root 4 Dec  8 08:36 .
drwxr-xr-x 6 root root 6 Dec  8 08:36 ..
drwxr-xr-x 2 root root 2 Dec  8 08:36 media
drwxr-xr-x 7 root root 8 Dec  8 08:40 static

root@yunohost:~# ls -la /opt/yunohost/Django Example/
total 58
drwxr-xr-x 5 Django Example Django Example   11 Dec  8 08:39 .
drwxr-xr-x 3 root        root           3 Dec  8 08:36 ..
-rw-r--r-- 1 Django Example Django Example  460 Dec  8 08:39 gunicorn.conf.py
-rw-r--r-- 1 Django Example Django Example    0 Dec  8 08:39 local_settings.py
-rwxr-xr-x 1 Django Example Django Example  274 Dec  8 08:39 manage.py
-rw-r--r-- 1 Django Example Django Example  171 Dec  8 08:39 secret.txt
drwxr-xr-x 6 Django Example Django Example    6 Dec  8 08:37 venv
-rw-r--r-- 1 Django Example Django Example  115 Dec  8 08:39 wsgi.py
-rw-r--r-- 1 Django Example Django Example 4737 Dec  8 08:39 settings.py

root@yunohost:~# cd /opt/yunohost/Django Example/
root@yunohost:/opt/yunohost/Django Example# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/Django Example# ./manage.py check
Django Example v0.8.2 (Django v2.2.17)
DJANGO_SETTINGS_MODULE='settings'
PROJECT_PATH:/opt/yunohost/Django Example/venv/lib/python3.7/site-packages
BASE_PATH:/opt/yunohost/Django Example
System check identified no issues (0 silenced).

root@yunohost:~# tail -f /var/log/Django Example/Django Example.log
root@yunohost:~# cat /etc/systemd/system/Django Example.service

root@yunohost:~# systemctl reload-or-restart Django Example
root@yunohost:~# systemctl status Django Example
root@yunohost:~# journalctl --unit=django_example --follow
```

## local test

For quicker developing of Django Example in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone https://github.com/YunoHost-Apps/django_example_ynh.git
~$ cd Django Example_ynh/
~/Django Example_ynh$ make
install-poetry         install or update poetry
install                install Django Example via poetry
update                 update the sources and installation
local-test             Run local_test.py to run Django Example_ynh locally
~/Django Example_ynh$ make install-poetry
~/Django Example_ynh$ make install
~/Django Example_ynh$ make local-test
```

Notes:

* SQlite database will be used
* A super user with username `test` and password `test` is created
* The page is available under `http://127.0.0.1:8000/app_path/`