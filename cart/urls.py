from django.urls import path, include

from order.views import CheckoutView
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('/checkout', CheckoutView.as_view(), name='checkout')
]
