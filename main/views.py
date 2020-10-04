from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import View
from catalog import models
from .models import Mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

LANGUAGES = ['ru', 'en']


def email_and_search(request, url_name, *args):
    email = request.POST.get('mail_to_send')
    search = request.POST.get('search')

    if email is not None:
        try:
            mail = Mail(mail=email)
            mail.save()
        except IntegrityError:
            pass
        if len(args) > 1:
            return redirect(url_name, args)
        if len(args) == 1:
            return redirect(url_name, args[0])
        return redirect(url_name)

    if search is not None and search is not '':
        return redirect('catalog', search)


def email_check(request, url_name, *args):
    email = request.POST.get('mail_to_send')
    if email is not None:
        try:
            mail = Mail(mail=email)
            mail.save()
        except IntegrityError:
            pass
        if len(args) > 1:
            return redirect(url_name, args)
        if len(args) == 1:
            return redirect(url_name, args[0])
        return redirect(url_name)


class MainView(View):
    def get(self, request, language=None):
        categories = models.Category.objects.all()
        items = models.Item.objects.filter(featured=True)[:16]
        context = {'categories': categories,
                   'items': items,
                   }

        if language in LANGUAGES:
            context['language'] = language
        elif request.headers['Accept-Language'][:2] in LANGUAGES:
            context['language'] = request.headers['Accept-Language'][:2]
        else:
            context['language'] = 'en'

        return render(request, 'main/home_page.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'main')
        return u_redirect
