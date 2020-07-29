from django.template import Library

register = Library()


@register.filter
def abc(text, symbols):
    if len(text) > symbols:
        return f'{text[:int(symbols)]}...'
    return text
