from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from main.views import generate_context, email_and_search
from order import models


class OrderView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request, order_id):
        context = generate_context(request)
        order = models.Order.objects.get(id=order_id)

        if order.user != request.user:
            return redirect('orders')

        context['order'] = order
        return render(request, 'order/order.html', context)

    def post(self, request, order_id):
        u_redirect = email_and_search(request, 'orders', order_id)
        if u_redirect is not None:
            return u_redirect

        return redirect('orders')


class CheckoutView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request):
        context = generate_context(request)
        return render(request, 'order/checkout.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'checkout')
        if u_redirect is not None:
            return u_redirect

        return redirect('checkout')
