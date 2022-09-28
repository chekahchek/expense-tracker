from django import template

register = template.Library()

@register.filter(name='replaceAndTitle')
def replaceAndTitle(value, arg):
    return value.replace(arg, ' ').title()
