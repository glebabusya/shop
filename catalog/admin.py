from django.contrib import admin
from . import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    actions = ['set_featured', 'set_unfeatured']

    def set_featured(self, request, queryset):
        queryset.update(featured=True)

    def set_unfeatured(self, request, queryset):
        queryset.update(featured=False)


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass
