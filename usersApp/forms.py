from django.contrib.auth.forms import UserCreationForm
from django.forms import CheckboxInput, ModelForm

from usersApp.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs') and not isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class RegistrationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

