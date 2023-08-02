from django import template
from django.utils.timesince import timesince

register = template.Library()

# 0 minutos -> primera vez
# 1 minutos -> siempre

@register.filter
def replace_minutes(timesince_last_message):
    minutes = ' '.join(timesince_last_message.split()[-2:])  # supuestamente
    leftover = ' '.join(timesince_last_message.split()[:-2])

    if minutes == '0 minutes':
        return "unos segundos"
    elif minutes == '1 minutos':
        return leftover + '1 minuto'

    timesince_last_message = timesince_last_message.replace('minutes', 'minutos')

    # extra
    last_comma_index = timesince_last_message.rfind(',')
    if last_comma_index >= 0:
        timesince_last_message = timesince_last_message[:last_comma_index] + ' y' + timesince_last_message[last_comma_index + 1:]

    return timesince_last_message
