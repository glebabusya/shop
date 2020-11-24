from django.contrib import admin

from order.models import PaymentType, Order, OrderItem


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass
