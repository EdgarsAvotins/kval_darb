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
    return 28 - days


@register.filter(name='get_full_name')
def get_full_name(username, users):
    for user in users:
        if str(user.username) == str(username):
            return user.first_name + ' ' + user.last_name
    return None

@register.filter(name='get_iesniegums_url')
def get_iesniegums_url(ieraksts, failu_saraksts):
    for fails in failu_saraksts:
        if fails.ieraksts.id == ieraksts.id:
            print fails.iesniegums.url
            return fails.iesniegums.url
    return None

@register.filter(name='get_atskaite_url')
def get_atskaite_url(ieraksts, failu_saraksts):
    for fails in failu_saraksts:
        if fails.ieraksts.id == ieraksts.id:
            return fails.atskaite.url
    return None

@register.filter(name='get_ceks_url')
def get_ceks_url(ieraksts, failu_saraksts):
    for fails in failu_saraksts:
        if fails.ieraksts.id == ieraksts.id:
            return fails.ceks.url
    return None