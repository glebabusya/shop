from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.MailToSendNews)
class MailAdmin(admin.ModelAdmin):
    pass
