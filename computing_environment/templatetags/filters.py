from datetime import date
from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='only_name')
def only_name(file):
    name = file.split('/')[-1]
    data_name = name.split('_')[0]+"-"+name.split('_')[-1]
    return data_name

@register.filter(name='days_between')
def days_between(up_date):
    today = date.today()
    return (today - up_date).days

@register.filter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()