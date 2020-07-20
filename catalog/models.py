from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField(max_length=400)
    description = models.CharField(max_length=1000, default=None, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=400, default=None, null=True)
    original_price = models.DecimalField(max_digits=9, decimal_places=2, default=None, null=True, )
    discount = models.PositiveIntegerField(help_text='%')
    amount = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=3000, default=None, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    # images
    image_1 = models.ImageField(upload_to='images %y-%m-%d-%H', null=True, default=None)
    image_2 = models.ImageField(upload_to='images %y-%m-%d-%H', null=True, default=None)
    image_3 = models.ImageField(upload_to='images %y-%m-%d-%H', null=True, default=None)

    def __str__(self):
        return f'{str(self.category)}-{self.name}'

    def price(self):
        return self.original_price - (self.original_price * self.discount / 100)


def rating_check(rate):
    if rate < 0 or rate > 5:
        raise ValidationError('Слишком большой рейтинг')


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=2000, null=True, default=None)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_query_name="comment")
    rating = models.IntegerField(validators=[rating_check])

    def __str__(self):
        return f'комментарий от {self.user} на {str(self.item)}: {self.comment[:15]} '
