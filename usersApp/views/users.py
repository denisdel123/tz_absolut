from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import generic

from usersApp.forms import RegistrationForm
from usersApp.models import User
from usersApp.services import all_send_mail


def main(request):
    return render(request, 'usersApp/base.html')


def send_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = 'Подтверждение Почты'
        code = get_random_string(4)
        massage = f'ваше код-слово {code}'
        email_list = [email]
        all_send_mail(subject, massage, email_list)

        request.session['confirmation_code'] = code
        request.session['user_email'] = email

        return redirect('usersApp:confirm')

    else:
        # Отображение страницы с формой для отправки
        # Замените 'send_code.html' на имя вашего HTML-шаблона
        return render(request, 'usersApp/send_word.html')


def email_confirm(request):
    if request.method == 'POST':
        code = request.POST.get('text')
        saved_code = request.session.get('confirmation_code')
        user_email = [request.session.get('user_email')]

        if saved_code == code:
            user = User.objects.create(email=user_email,)
            passw = get_random_string(9)
            user.set_password(passw)
            user.save()
            subject = 'Поздравляем с регистрацией!'
            massage = f'ваш пароль: {passw}'
            all_send_mail(subject, massage, user_email)

            del request.session['confirmation_code']
            del request.session['user_email']

            return redirect('usersApp:main')

        else:
            messages.error(request, 'не верный код попробуйте снова!')

        return render(request, 'usersApp/confirm.html')

    else:
        return render(request, 'usersApp/confirm.html')
