from django.apps import AppConfig


class {{ cookiecutter.verbose_name }}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{ cookiecutter.package_name }}'
