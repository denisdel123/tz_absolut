from django.urls import path

from mainApp.apps import MainappConfig
from mainApp.views import main

app_name = MainappConfig.name
urlpatterns = [
    path('', main, name='main'),
]