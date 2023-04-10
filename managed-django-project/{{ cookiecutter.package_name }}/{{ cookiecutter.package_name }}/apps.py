from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = '{{ cookiecutter.package_name }}'
    verbose_name = '{{ cookiecutter.project_name }}'

    def ready(self):
        import {{ cookiecutter.package_name }}.checks  # noqa
