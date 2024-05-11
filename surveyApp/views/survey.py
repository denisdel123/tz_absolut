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


class SurveyUpdateView(generic.UpdateView):
    model = Survey
    form_class = SurveyForm


class SurveyDeleteView(generic.DeleteView):
    model = Survey
    template_name = 'surveyApp/survey_confirm_delete.html'
    success_url = 'usersApp:main'
