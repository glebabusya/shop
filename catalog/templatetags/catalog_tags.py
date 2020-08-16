from django.template import Library
from .. import models

register = Library()


@register.filter
def cut(text, symbols):
    if len(text) > symbols:
        return f'{text[:int(symbols)]}...'
    return text


@register.filter
def number_round(text):
    return round(int(text))


@register.simple_tag
def average_price(list):
    price = 0
    try:
        for item in list:
            price += item.price()
        return price
    except:
        return False


@register.simple_tag
def rating_amount(item, rating):
    return item.comment_set.filter(rating=rating).count()


@register.simple_tag
def rating_percent(item, rating):
    item_rating_amount = item.comment_set.filter(rating=rating).count()
    if item_rating_amount == 0:
        return 0
    all_rating = item.comment_set.all().count()
    return (item_rating_amount / all_rating) * 100
