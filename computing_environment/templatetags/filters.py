from datetime import datetime
from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='only_name')
def only_name(file):
    name = file.split('/')[-1].split('_')
    data_name = name[-1] # name[0]+"-"+name[-1]
    return data_name

@register.filter(name='minutes_between')
def minutes_between(up_date):
    today = datetime.now(up_date.tzinfo)
    secs_between = (today - datetime(up_date.year, up_date.month, up_date.day, up_date.hour, up_date.minute, up_date.second, tzinfo=up_date.tzinfo)).seconds
    return secs_between / 60

@register.filter(name='modulo')
def modulo(num, val=60):
    return num % val

@register.filter(name='replace_floor')
def replace_floor(text):
    return text.replace('_', ' ')

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

@register.filter(name='nice_timedelta')
def nice_timedelta(timedelta):
    seconds = timedelta
    nice_time = ""

    if seconds > 86400:
        days = seconds // 86400
        nice_time += f"{int(days)} days "
        seconds = seconds - days*86400

    if seconds > 3600:
        hours = seconds // 3600
        nice_time += f"{int(hours)} h "
        seconds = seconds - hours*3600

    if seconds > 60:
        minutes = seconds // 60
        nice_time += f"{int(minutes)} min "
        seconds = seconds - minutes*60

    if seconds > 0:
        nice_time += f"{int(seconds)} s "
    return nice_time