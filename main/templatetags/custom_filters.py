from django import template

register = template.Library()

@register.filter
def upto(value):
    return range(1, value + 1)


@register.filter
def custom_range(value):
    return range(value)

@register.filter
def mul(value, arg):
    return value * arg