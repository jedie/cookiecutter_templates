from django.http import HttpResponse

from your_reuseable_django_app import __version__


def hello_world(request):
    return HttpResponse(f'Hello, world! From your_reuseable_django_app v{__version__}')
