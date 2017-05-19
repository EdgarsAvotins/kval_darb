from django import template
import datetime

register = template.Library()


@register.filter(name='is_found')
def if_found(ieraksts, komandejumi):
    found = False
    for kom in komandejumi:
        if kom.ieraksts.id == ieraksts.id:
            found = True
    return found

@register.filter(name='trip_ended')
def trip_ended(datums_lidz):
    now = datetime.datetime.now()
    return datums_lidz <= now.date()
