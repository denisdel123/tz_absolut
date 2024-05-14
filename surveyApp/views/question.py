from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from surveyApp.forms import QuestionForm, ChoiceTypeForm, TextTypeForm
from surveyApp.models import Question, Survey

choices_business_subcategory = {

    'sale': [
        ('retail', 'Розничная торговля'),
        ('wholesale', 'Оптовая торговля'),
        ('online_store', 'Интернет-магазин'),
        ('market_sale', 'Продажа на рынке'),
    ],
    'services': [
        ('consulting', 'Консультационные услуги'),
        ('education', 'Образовательные услуги'),
        ('medical', 'Медицинские услуги'),
        ('transport', 'Транспортные услуги'),
        ('repair', 'Ремонтные услуги'),
    ],
    'production': [
        ('food', 'Производство продуктов питания'),
        ('industrial', 'Промышленное производство'),
        ('construction_materials', 'Производство строительных материалов'),
    ],
    'entertainment': [
        ('restaurants', 'Рестораны и кафе'),
        ('theaters', 'Кинотеатры и театры'),
        ('fitness', 'Спортивные клубы и фитнес-центры'),
        ('tourism_business', 'Туристический бизнес'),
    ],
    'finance': [
        ('banks', 'Банки и финансовые институты'),
        ('investment', 'Инвестиционные компании'),
        ('insurance', 'Страховые компании'),
    ],
    'technologies': [
        ('it', 'IT-компании'),
        ('telecom', 'Телекоммуникационные услуги'),
        ('software', 'Разработка программного обеспечения'),
        ('web_dev', 'Веб-разработка'),
    ],
    'tourism': [
        ('hotels', 'Отели и гостиницы'),
        ('agencies', 'Туристические агентства'),
        ('rental', 'Аренда жилья'),
        ('excursions', 'Экскурсионные компании'),
    ],
    'education': [
        ('schools', 'Школы и университеты'),
        ('additional_education', 'Дополнительное образование'),
        ('language_schools', 'Языковые школы'),
        ('online_education', 'Онлайн-образование'),
    ],
    'healthcare': [
        ('hospitals', 'Больницы и клиники'),
        ('pharmacies', 'Аптеки'),
        ('private_practice', 'Частная практика'),
    ],

    'business': [
        ('sale', 'Продажа товаров'),
        ('services', 'Услуги'),
        ('production', 'Производство'),
        ('entertainment', 'Развлечения и досуг'),
        ('finance', 'Финансы и банковские услуги'),
        ('technologies', 'Технологии и информационные услуги'),
        ('tourism', 'Туризм и гостеприимство'),
        ('education', 'Образование'),
        ('healthcare', 'Здравоохранение'),
    ]
}


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


def ask(request):
    survey = Survey.objects.first()
    questions = survey.questions.all()

    answered_questions = request.session.get('answered_questions', [])
    print(answered_questions)

    next_question = None
    for question in questions:
        print(question)

        if question.pk not in answered_questions:
            next_question = question
            break

    if next_question:

        if next_question.question_type == 'text':
            form = TextTypeForm()
            return render(request, 'surveyApp/question_text.html', {'form': form, 'question': next_question})


        else:

            late_answer = request.session.get('late_answer')
            if late_answer:
                options = choices_business_subcategory[late_answer]
            else:
                options = choices_business_subcategory['business']

            print(late_answer)

            form = ChoiceTypeForm(question=next_question, options=options)
            return render(request, 'surveyApp/question_choice.html',
                          {'form': form, 'question': next_question})

    else:
        return redirect('surveyApp:survey_completed')
