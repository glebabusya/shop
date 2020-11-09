import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers import exception
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import View
from main.views import email_and_search, generate_context
from .. import forms, models
from ..models import VarificationCode, FavoriteItem


def adding_to_wishlist(item, user):
    try:
        models.FavoriteItem.objects.get(item=item, user=user)
    except models.FavoriteItem.DoesNotExist:
        f_item = models.FavoriteItem(item=item, user=user)
        f_item.save()


class OrdersView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request):
        context = generate_context(request)
        return render(request, 'account/orders.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'orders')
        if u_redirect is not None:
            return u_redirect


class ProfileView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request):
        context = generate_context(request)
        user = request.user
        form = forms.ProfileForm(instance=user)
        context['form'] = form
        return render(request, 'account/profile.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'profile')
        if u_redirect is not None:
            return u_redirect

        user = request.user
        form = forms.ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = user.email
            new_user.save()
        else:
            messages.error(request, 'Enter the valid Phone')

        return redirect('profile')


class WishListView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request):
        context = generate_context(request)
        user = request.user

        f_items = models.FavoriteItem.objects.filter(user=user)
        context['f_items'] = f_items

        return render(request, 'account/wishlist.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'wishlist')
        if u_redirect is not None:
            return u_redirect

        user = request.user

        post = request.POST

        for key, value in post.items():
            if key[:5] == 'clear':
                models.FavoriteItem.objects.all().delete()

            if key[:6] == 'delete':
                item = models.Item.objects.get(name=key[7:])
                models.FavoriteItem.objects.get(user=user, item=item).delete()
        return redirect('wishlist')
