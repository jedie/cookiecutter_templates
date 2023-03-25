from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'your_cool_package'
    verbose_name = 'your_cool_package'

    def ready(self):
        import your_cool_package.checks  # noqa
