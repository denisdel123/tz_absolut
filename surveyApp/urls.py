from django.urls import path

from surveyApp.apps import SurveyappConfig
from surveyApp.views.survey import SurveyCreateView, SurveyUpdateView, SurveyDeleteView, SurveyListView, \
    SurveyDetailView

app_name = SurveyappConfig.name

urlpatterns = [
    # CRUD survey
    path('create/', SurveyCreateView.as_view(), name='create_survey'),
    path('list/', SurveyListView.as_view(), name='list_survey'),
    path('detail/<int:pk>/', SurveyDetailView.as_view(), name='detail_survey'),
    path('update/<int:pk>/', SurveyUpdateView.as_view(), name='update_survey'),
    path('delete/<int:pk>/', SurveyDeleteView.as_view(), name='delete_survey'),

]
