from django.urls import path

from {{ cookiecutter.package_name }}.views import hello_world


urlpatterns = [
    path('hello_world', hello_world, name='hello_world'),
]
