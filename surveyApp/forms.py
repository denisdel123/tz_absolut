from django.forms import CheckboxInput
from django import forms

from surveyApp.models import Survey, Question, Answer


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs') and not isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class SurveyForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('title', 'description',)


class QuestionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'question_type',)


class ChoiceTypeForm(StyleFormMixin, forms.ModelForm):
    my_choice_field = forms.ChoiceField(choices=[])
    choice_answer = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Answer
        fields = []

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        options = kwargs.pop('options', [])
        super().__init__(*args, **kwargs)

        if question:
            self.fields['my_choice_field'].choices = self.get_choices_for_question(question, options)

    def get_choices_for_question(self, question, options):
        return options


class TextTypeForm(StyleFormMixin, forms.ModelForm):
    my_text_field = forms.CharField()

    class Meta:
        model = Answer
        fields = ['text_answer']
