from django import template

register = template.Library()


@register.filter(name='is_found')
def if_found(ieraksts, komandejumi):
    found = False
    for kom in komandejumi:
        if kom.ieraksts.id == ieraksts.id:
            found = True
    return found