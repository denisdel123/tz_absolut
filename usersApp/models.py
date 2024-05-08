from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'null': True,
    'blank': True
}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    age = models.PositiveIntegerField(**NULLABLE, verbose_name='Возраст')
    country = models.CharField(max_length=100, **NULLABLE, verbose_name='Страна')
    city = models.CharField(max_length=100, **NULLABLE, verbose_name='Город')
    phone = models.CharField(max_length=20, **NULLABLE, verbose_name='Телефон')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
