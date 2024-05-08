from django.urls import path

from usersApp.apps import UsersappConfig
from usersApp.views.users import main, email_confirm, send_code

app_name = UsersappConfig.name

urlpatterns = [
    path('', main, name='main'),
    path('confirm/', email_confirm, name='confirm'),
    path('send/', send_code, name='send_code'),
]
