from django import template
from django.utils.timesince import timesince
from django.utils.translation import gettext

register = template.Library()

@register.filter
def timesince_es(value):
    result = timesince(value)

    # Modificación a unos segundos
    if '0' in result or '0 minutos' in result:
        return gettext('unos segundos')
    # Corrección de pluralización para '1 minutos'
    elif '1' in result or '1 minutos' in result:
        return gettext('1 minuto')

    # Traducción de 'minutes' a 'minutos'
    result = result.replace('minutes', gettext('minutos'))

    return result
