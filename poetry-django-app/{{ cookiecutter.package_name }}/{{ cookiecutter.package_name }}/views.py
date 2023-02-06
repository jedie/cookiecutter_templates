from django.http import HttpResponse

from {{ cookiecutter.package_name }} import __version__


def hello_world(request):
    return HttpResponse(f'Hello, world! From {{ cookiecutter.package_name }} v{__version__}')
