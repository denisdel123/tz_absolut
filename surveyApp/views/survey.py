from django.urls import reverse_lazy
from django.views import generic
from surveyApp.forms import SurveyForm
from surveyApp.models import Survey


class SurveyCreateView(generic.CreateView):
    model = Survey
    form_class = SurveyForm
    success_url = reverse_lazy('surveyApp:list_survey')


class SurveyListView(generic.ListView):
    model = Survey


class SurveyDetailView(generic.DetailView):
    model = Survey

    def get_success_url(self):
        object_id = self.object.pk
        detail_url = reverse_lazy('surveyApp:detail_survey', kwargs={'pk': object_id})
        return detail_url

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        survey = self.object
        question_list = survey.questions.all()
        context_data['questions'] = question_list
        return context_data


class SurveyUpdateView(generic.UpdateView):
    model = Survey
    form_class = SurveyForm

    def get_success_url(self):
        survey_id = self.object.pk
        detail_url = reverse_lazy('surveyApp:detail_survey', kwargs={'pk': survey_id})
        return detail_url


class SurveyDeleteView(generic.DeleteView):
    model = Survey
    success_url = reverse_lazy('surveyApp:list_survey')
