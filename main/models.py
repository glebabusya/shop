from django.db import models


# Create your models here.
class Mail(models.Model):
    mail = models.EmailField(unique=True)
