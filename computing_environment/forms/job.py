from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from ..constants import LANGUAGES
from ..models import Job

class JobForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGES)

    class Meta:
        model = Job
        fields = ['name', 'language', 'program', 'settings', 'is_private']
        widgets = {
            'name': widgets.TextInput(attrs={"placeholder": "Job Name"}),
            'settings': widgets.Textarea(attrs={ "placeholder": '{\n"setting": "value"\n}'})
        }

    def clean_language(self):
        language = self.cleaned_data['language']
        if not language in map(lambda l: l[0], LANGUAGES):
            raise ValidationError(
                ('%(value)s is not valid language'),
                code='invalid',
                params={'value': language},
            )

        return language