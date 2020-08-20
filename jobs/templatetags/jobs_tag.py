from django import template

register = template.Library()

@register.filter()
def jobs_tag(value):
    return value.__class__.__name__
