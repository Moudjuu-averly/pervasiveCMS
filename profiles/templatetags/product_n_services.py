from django import template

register = template.Library()

@register.filter()
def product_n_services(value):
    return value.__class__.__name__
