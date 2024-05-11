from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from surveyApp.forms import QuestionForm
from surveyApp.models import Question, Survey


class QuestionCreateView(generic.CreateView):
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        survey_id = int(self.request.GET.get('survey_id'))

        if survey_id:
            print(survey_id)
            survey = Survey.objects.get(pk=survey_id)
            print(survey)
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
