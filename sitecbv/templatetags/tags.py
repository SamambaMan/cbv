from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def contexto(value):
    if value.__class__.__name__ == 'ConteudoExclusivo':
        return 'conteudoexclusivo'
    if value.__class__.__name__ == 'Experiencia':
        return 'experiencias'
    if value.__class__.__name__ == 'CensoDoVolei':
        return 'censosvolei'
    return None

@register.filter
def primeironome(value):
    if not value:
        return ""

    return value.split(" ")[0]
