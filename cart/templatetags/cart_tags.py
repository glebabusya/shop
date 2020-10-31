from django.template import Library
from .. import models

register = Library()


@register.simple_tag
def average_price(items):
    total_price = 0
    for item in items:
        total_price += float(item.item.price()) * item.amount
    return total_price.__round__(4)


@register.simple_tag
def subtotal_item_price(item):
    total_price = item.item.price() * item.amount
    return total_price


@register.simple_tag
def discount_check(item):
    total_discount = (item.item.original_price - item.item.price()) * item.amount
    return total_discount


@register.simple_tag
def coupon(items, coupon):
    price = average_price(items)
    if coupon != 0:
        return f'<span class="muted-text text-crossed">${price}</span> <span>${(price * (1 - coupon.discount / 100)).__round__(4)}</span>'
    return price.__round__(4)
