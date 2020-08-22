from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Mail)
class MailAdmin(admin.ModelAdmin):
    pass
