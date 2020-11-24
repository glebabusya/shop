from django.conf import settings
from django.db import models
from django.utils import timezone

from account.models import ShopUser
from catalog.models import Item


class PaymentType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def price(self):
        return self.item.price() * self.amount

    def __str__(self):
        return f'{self.item.name} ({self.amount})'


class Order(models.Model):
    items = models.ManyToManyField(OrderItem, blank=True)
    created_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, blank=True, null=True, default=None)
    coupon = models.ForeignKey('cart.Coupon', on_delete=models.CASCADE, blank=True, default=None, null=True)

    STATES = [
        ('new', 'New order'),
        ('accepted', 'Order accepted'),
        ('rejected', 'Order rejected'),
        ('shipping', 'Shipping order'),
        ('delivered', 'Order delivered'),
    ]

    state = models.CharField(max_length=20, choices=STATES, default='new')

    def review(self):
        self.state = 'in_review'

    def accept(self):
        self.state = 'accepted'

    def reject(self):
        self.state = 'rejected'

    def ship(self):
        self.state = 'shipping'

    def deliver(self):
        self.state = 'delivered'

    def drop(self):
        self.state = 'dropped'

    def get_total_price(self):
        price = 0
        items = self.items.all()

        for item in items:
            price += item.price()

        if self.coupon:
            price = price * (100 - self.coupon.discount) / 100

        return price
