from django import template
from num2words import num2words

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter
def number_to_words(value):
    try:
        value = int(value)
        return num2words(value)
    except (ValueError, TypeError):
        return value