from django.forms import CheckboxInput
from django import forms

from surveyApp.models import Survey


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
