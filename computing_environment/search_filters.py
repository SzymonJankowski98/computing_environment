import django_filters 
from .models import Job
from django import forms

class JobFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Job
        fields = ['name', 'state']
