from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from ..constants import LANGUAGES
from ..models import Job
import json

class JobForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGES)
    settings = forms.CharField(label='Settings', required=False,
        widget = forms.Textarea(
            attrs= {
              'placeholder': '{\n"setting": "value"\n}'
            }
        )
    )

    class Meta:
        model = Job
        fields = ['name', 'language', 'program', 'is_private']
        widgets = {
            'name': widgets.TextInput(attrs={"placeholder": "Job Name"})
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
    
    def clean_settings(self):
        settings = self.cleaned_data['settings']
        if not settings:
            raise forms.ValidationError("JSON cannot be empty")
        try:
            json.loads(settings)
        except:
            raise forms.ValidationError("Invalid JSON")
        if not type(json.loads(settings)) == list:
            raise forms.ValidationError("JSON outer element must be a list")

        return settings

class EditJobForm(JobForm):
    def clean_settings(self):
        settings = self.cleaned_data['settings']
        print(settings)
        if settings == '':
            return settings
        try:
            json.loads(settings)
        except:
            raise forms.ValidationError("Invalid JSON")
        if not type(json.loads(settings)) == list:
            raise forms.ValidationError("JSON outer element must be a list")

        return settings