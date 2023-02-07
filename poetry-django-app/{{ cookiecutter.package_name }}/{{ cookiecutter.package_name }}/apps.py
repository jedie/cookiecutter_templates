from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = '{{ cookiecutter.package_name }}'
    verbose_name = '{{ cookiecutter.package_name }}'
