from django import forms
from django.forms import fields
from ..models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'program', 'settings', 'is_private']
