from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from catalog.models import Item
from main.views import email_and_search, generate_context
from order.models import OrderItem, Order
from . import models


def adding_to_cart(user, item, amount):
    """function of adding items to cart"""
    try:
        item = models.CartItem.objects.get(user=user, item=item)

        item.amount = amount + item.amount
        if item.amount > 20:
            item.amount = 20
    except models.CartItem.DoesNotExist:
        item = models.CartItem(user=user, item=item, amount=amount)
    item.save()


class CartView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request):
        context = generate_context(request)
        try:
            coupon = models.Coupon.objects.get(name=request.session.get('_coupon'))
        except models.Coupon.DoesNotExist:
            coupon = None
        context['coupon'] = coupon

        return render(request, 'cart/cart.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'cart')
        if u_redirect is not None:
            return u_redirect

        request.session['_coupon'] = request.POST.get('coupon')

        post = request.POST
        user = request.user
        items = models.CartItem.objects.filter(user=user)

        for key, value in post.items():  # updating items in cart
            if key[:5] == 'clear':
                items.delete()

            if key[:6] == 'delete':
                item = Item.objects.get(name=key[7:])
                models.CartItem.objects.get(user=user, item=item).delete()

            if key[:6] == 'amount':
                item = Item.objects.get(name=key[7:])
                add_item = models.CartItem.objects.get(user=user, item=item)
                add_item.amount = value if int(value) <= 20 else 20

                add_item.save()

            if key[:4] == 'make':
                order = Order(user=user)
                order.save()
                for item in items:
                    order_item = OrderItem(item=item.item, amount=item.amount)
                    order_item.save()
                    order.items.add(order_item.id)
                    order.save()
                items.delete()
                return redirect('checkout')
        try:
            models.Coupon.objects.get(name=request.session.get('_coupon'))
            messages.success(request, 'Coupon applied')
        except models.Coupon.DoesNotExist:
            pass

        return redirect('cart')
