from django.urls import path

from usersApp.apps import UsersappConfig
from usersApp.views.users import email_confirm, send_code, Logout, Login, UserDetailView

app_name = UsersappConfig.name

urlpatterns = [

    # Подтверждение почты и регистрация пользователя
    path('send_code/', send_code, name='send_code'),
    path('confirm/', email_confirm, name='confirm'),


    # Вход и выход пользователя
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    # Профиль пользователя
    path('detail/<int:pk>', UserDetailView.as_view(), name='detail_user')

]
