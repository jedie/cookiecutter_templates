## Settings and upgrades

Almost everything related to {{ cookiecutter.project_name }}'s configuration is handled in a `"../conf/settings.py"` file.
You can edit the file `/home/yunohost.app/{{ cookiecutter.project_id }}/local_settings.py` to enable or disable features.

Test sending emails, e.g.:

```bash
ssh admin@yourdomain.tld
root@yunohost:~# /home/yunohost.app/{{ cookiecutter.upstream_pkg_name }}/manage.py sendtestemail --admins
```

How to debug a django YunoHost app, take a look into:

* https://github.com/YunoHost-Apps/django_example_ynh#developer-info
