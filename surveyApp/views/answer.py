from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from surveyApp.models import Answer, Survey, Question
from usersApp.models import User


class AnswerCreateView(generic.CreateView):
    model = Answer
    fields = ['text_answer']
    template_name = 'surveyApp/question_text.html'

    def form_valid(self, form):
        new_answer = form.save(commit=False)
        answer = self.request.POST.get('answer')
        user_email = self.request.session.get('user_email')
        question_id = self.request.POST.get('question_id')
        question = Question.objects.get(pk=question_id)
        user = User.objects.get(email=user_email)
        new_answer.text_answer = answer
        new_answer.user = user
        new_answer.question = question
        new_answer.save()
        answered_questions = self.request.session.get('answered_questions', [])
        answered_questions.append(question_id)
        self.request.session['answered_questions'] = answered_questions

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('surveyApp:question_text')


def completed(request):
    del request.session['user_email']
    del request.session['answered_questions']

    return redirect('usersApp:login')
