from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from surveyApp.forms import TextTypeForm, ChoiceTypeForm
from surveyApp.models import Answer, Survey, Question
from usersApp.models import User




class AnswerCreateView(generic.CreateView):
    model = Answer
    fields = ['text_answer', 'choice_answer']

    def form_valid(self, form):
        new_answer = form.save(commit=False)
        user_email = self.request.session.get('user_email')
        question_id = int(self.request.POST.get('question_id'))
        user = User.objects.get(email=user_email)

        if not question_id:
            form.add_error(None, 'Идентификатор вопроса отсутствует.')
            return self.form_invalid(form)

        try:
            question_id = int(question_id)
            question = Question.objects.get(pk=question_id)
        except ValueError:
            form.add_error(None, 'Идентификатор вопроса неверный.')
            return self.form_invalid(form)
        except Question.DoesNotExist:
            form.add_error(None, 'Вопрос не найден.')
            return self.form_invalid(form)

        if question.question_type == 'choice':
            answer = self.request.POST.get('my_choice_field')
            new_answer.choice_answer = answer
            self.request.session['late_answer'] = answer

        elif question.question_type == 'text':
            new_answer.text_answer = self.request.POST.get('answer')

        new_answer.user = user
        new_answer.question = question
        new_answer.save()

        answered_questions = self.request.session.get('answered_questions', [])
        answered_questions.append(question_id)
        self.request.session['answered_questions'] = answered_questions

        return super().form_valid(form)

    def get_success_url(self):
        question_id = self.request.POST.get('question_id')
        question = Question.objects.get(pk=question_id)

        if question.question_type == 'text':
            return reverse_lazy('surveyApp:question_text')

        else:
            return reverse_lazy('surveyApp:question_choice')

    def get_template_names(self):
        question_id = self.request.GET.get('question_id') or self.request.POST.get('question_id')
        question = Question.objects.get(pk=question_id)
        if question.question_type == 'text':
            return ['surveyApp/question_text.html']
        else:
            return ['surveyApp/question_choice.html']


def completed(request):
    del request.session['user_email']
    del request.session['answered_questions']
    del request.session['late_answer']

    return redirect('usersApp:login')
