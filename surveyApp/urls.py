from django.urls import path

from surveyApp.apps import SurveyappConfig
from surveyApp.views.answer import AnswerCreateView, completed
from surveyApp.views.question import QuestionCreateView, QuestionListView, QuestionDeleteView, QuestionUpdateView, ask
from surveyApp.views.survey import SurveyCreateView, SurveyUpdateView, SurveyDeleteView, SurveyListView, \
    SurveyDetailView

app_name = SurveyappConfig.name

urlpatterns = [
    # CRUD survey
    path('create/survey/', SurveyCreateView.as_view(), name='create_survey'),
    path('list/survey/', SurveyListView.as_view(), name='list_survey'),
    path('detail/survey/<int:pk>/', SurveyDetailView.as_view(), name='detail_survey'),
    path('update/survey/<int:pk>/', SurveyUpdateView.as_view(), name='update_survey'),
    path('delete/survey/<int:pk>/', SurveyDeleteView.as_view(), name='delete_survey'),

    # CRUD question
    path('create/question/', QuestionCreateView.as_view(), name='create_question'),
    path('list/question/', QuestionListView.as_view(), name='list_question'),
    path('update/question/<int:pk>/', QuestionUpdateView.as_view(), name='update_question'),
    path('delete/question/<int:pk>/', QuestionDeleteView.as_view(), name='delete_question'),

    # Answer
    path('question/text/', ask, name='question_text'),
    path('answer/create/', AnswerCreateView.as_view(), name='answer_create'),
    path('survey/completed/', completed, name='survey_completed'),

]
