from django import forms
from django.forms import fields, widgets
from ..models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'program', 'settings', 'is_private']
        widgets = {
            'name': widgets.TextInput(attrs={"placeholder": "Job Name"}),
            'settings': widgets.Textarea(attrs={ "placeholder": '{\n"setting": "value"\n}'})
        }
