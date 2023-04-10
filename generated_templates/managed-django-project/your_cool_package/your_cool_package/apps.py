from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'your_cool_package'
    verbose_name = 'your-cool-package'

    def ready(self):
        import your_cool_package.checks  # noqa
