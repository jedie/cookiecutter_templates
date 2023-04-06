from django.urls import path

from your_reuseable_django_app.views import hello_world


urlpatterns = [
    path('hello_world', hello_world, name='hello_world'),
]
