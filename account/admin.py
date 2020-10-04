from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ShopUserCreationForm, ShopUserChangeForm
from .models import ShopUser, VarificationCode


class ShopUserAdmin(UserAdmin):
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(ShopUser, ShopUserAdmin)


@admin.register(VarificationCode)
class VarificationCodeAdmin(admin.ModelAdmin):
    pass
