from django.conf import settings
from django.db import models

from catalog.models import Item


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.item.name

    def price(self):
        return self.item.price() * self.amount


class Coupon(models.Model):
    name = models.CharField(max_length=20)
    discount = models.IntegerField(help_text='%')

    def __str__(self):
        return self.name
