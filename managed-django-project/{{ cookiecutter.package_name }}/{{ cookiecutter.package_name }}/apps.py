from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = '{{ cookiecutter.package_name }}'
    verbose_name = '{{ cookiecutter.package_name }}'

    def ready(self):
        import {{ cookiecutter.package_name }}.checks  # noqa
