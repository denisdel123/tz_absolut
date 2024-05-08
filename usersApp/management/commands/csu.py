import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from usersApp.models import User

load_dotenv()
EMAIL_SUPERUSER = os.environ.get('EMAIL_SUPERUSER')
PASS_SUPERUSER = os.environ.get('PASS_SUPERUSER')

"""Создание администратора."""


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        superuser = User.objects.create(
            first_name='Admin',
            email=EMAIL_SUPERUSER,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        superuser.set_password(PASS_SUPERUSER)
        superuser.save()


