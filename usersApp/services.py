from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from app.settings import ADDRESS_MAIL_RU


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



