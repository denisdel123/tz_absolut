from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import generic

from usersApp.models import User
from usersApp.services import all_send_mail, confirm_email, create_secret_code


class Login(LoginView):
    template_name = 'usersApp/login.html'


class Logout(LogoutView):
    pass


class UserDetailView(generic.DetailView):
    model = User

    def get_success_url(self):
        object_id = self.object.pk
        detail_url = reverse_lazy('usersApp:detail_user', kwargs={'pk': object_id})
        return detail_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["user"] = self.request.user
        return context


def send_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return render(request, 'usersApp/send_word.html',
                          {'email': email, 'messages': messages.get_messages(request)})
        else:
            code = create_secret_code()
            subject = 'Подтверждение Почты'
            massage = f'ваше код-слово {code}'
            all_send_mail(subject, massage, [email])

            request.session['confirmation_code'] = code
            request.session['user_email'] = email

            return redirect('usersApp:confirm')

    else:
        action = reverse('usersApp:send_code')
        return render(request, 'usersApp/send_word.html', {"action": action})


def email_confirm(request):
    if request.method == 'POST':
        code = request.POST.get('text')
        saved_code = request.session.get('confirmation_code')
        user_email = request.session.get('user_email')

        if confirm_email(code, saved_code):
            user = User.objects.create(email=user_email, )
            passw = get_random_string(9)
            user.set_password(passw)
            user.save()

            subject = 'Поздравляем с регистрацией!'
            massage = f'ваш пароль: {passw}'
            all_send_mail(subject, massage, [user_email])

            del request.session['confirmation_code']

            # ссылаться на опрос с вопросами
            return redirect('surveyApp:question_text')

        else:
            messages.error(request, 'не верный код попробуйте снова!')

        return render(request, 'usersApp/confirm.html')

    else:
        action = reverse("usersApp:confirm")
        return render(request, 'usersApp/confirm.html', {'action': action})


class ChangePassword(PasswordChangeView):
    template_name = "usersApp/change_password.html"
    success_url = reverse_lazy('mainApp:main')
