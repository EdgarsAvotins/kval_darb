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

@register.filter(name='days_between')
def days_between(datums_no, datums_lidz):
    days = datums_lidz - datums_no
    return days.days + 1

@register.filter(name='vacation_days_left')
def vacation_days_left(ieraksti):
    days = 0
    for ieraksts in ieraksti:
        if ieraksts.merkis == 'atvalinajums':
            counter = ieraksts.datums_lidz - ieraksts.datums_no
            days = days + counter.days + 1

    return 30 - days
