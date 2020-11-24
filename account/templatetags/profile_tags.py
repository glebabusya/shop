from django.template import Library

register = Library()


@register.simple_tag
def full_name(user):
    result = ''
    if user.first_name is not None:
        result += user.first_name
    if user.last_name is not None:
        result += ' ' + user.last_name
    if not result:
        result += user.username
    return result
