from django.core.mail import send_mail
import random
from app.settings import ADDRESS_MAIL_RU

"""Отправление сообщения на почту клиенту"""


def all_send_mail(subject, massage, email):
    try:
        send_mail(
            subject=subject,
            message=massage,
            recipient_list=email,
            from_email=ADDRESS_MAIL_RU
        )
        return True
    except Exception:
        return False


"""Генерация секретного кода и отправление на почту."""


def create_secret_code():
    code = ''.join(random.choices('0123456789', k=4))
    return code


"""Отправляет секретный код"""


def send_secret_code(email, code):
    subject = 'Подтверждение Почты'
    massage = f'ваше код-слово {code}'
    email_list = [email]
    all_send_mail(subject, massage, email_list)


"""Проверка почты."""


def confirm_email(code, saved_code):
    if code == saved_code:
        return True
    else:
        return False
