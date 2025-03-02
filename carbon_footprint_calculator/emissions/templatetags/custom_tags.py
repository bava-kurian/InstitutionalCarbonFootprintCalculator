from django import template

register = template.Library()

@register.simple_tag
def range_custom(start, end):
    return range(start, end)
