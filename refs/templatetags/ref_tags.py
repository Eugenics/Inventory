from django import template

register = template.Library()


@register.filter
def in_list(value, list_of_values):
    value = str(value)
    return value in list_of_values.split(',')