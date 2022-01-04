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

@register.filter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]