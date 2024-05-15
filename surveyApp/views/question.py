import json
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from surveyApp.forms import QuestionForm, ChoiceTypeForm, TextTypeForm
from surveyApp.models import Question, Survey


class QuestionCreateView(generic.CreateView):
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        survey_id = int(self.request.GET.get('survey_id'))

        if survey_id:
            survey = Survey.objects.get(pk=survey_id)
            self.object = form.save(commit=False)
            self.object.survey = survey
            self.object.save()
            return redirect('surveyApp:detail_survey', pk=survey_id)

        else:
            return HttpResponseBadRequest('Идентификатор опроса не передан')


class QuestionListView(generic.ListView):
    model = Question


class QuestionUpdateView(generic.UpdateView):
    model = Question
    form_class = QuestionForm

    def get_success_url(self):
        survey_id = int(self.request.GET.get('survey_id'))
        detail_url = reverse_lazy('surveyApp:detail_survey', kwargs={'pk': survey_id})
        return detail_url


class QuestionDeleteView(generic.DeleteView):
    model = Question

    def get_success_url(self):
        survey_id = int(self.request.GET.get('survey_id'))
        detail_url = reverse_lazy('surveyApp:detail_survey', kwargs={'pk': survey_id})
        return detail_url


def ask(request):
    survey = Survey.objects.first()
    questions = survey.questions.all()

    answered_questions = request.session.get('answered_questions', [])

    next_question = None
    for question in questions:

        if question.pk not in answered_questions:
            next_question = question
            break

    if next_question:

        if next_question.question_type == 'text':
            form = TextTypeForm()
            return render(request, 'surveyApp/question_text.html', {'form': form, 'question': next_question})

        else:

            late_answer = request.session.get('late_answer')
            with open('choices.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            if late_answer:

                options = data[late_answer]
            else:
                options = data['business']

            form = ChoiceTypeForm(question=next_question, options=options)
            return render(request, 'surveyApp/question_choice.html',
                          {'form': form, 'question': next_question})

    else:
        return redirect('surveyApp:survey_completed')
