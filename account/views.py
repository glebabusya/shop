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
from main.views import email_and_search
from . import forms, models
from .models import VarificationCode


def hash_key(amount):
    result = ''
    variants = 'abcdefghjklmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ0123456789'
    for symbol in range(amount):
        result += random.choice(variants)
    return result


ATTEMPT_AMOUNT = 0


class RegLogView(View):
    def get(self, request):
        registration_form = forms.RegistrationForm()
        login_form = forms.LoginForm()
        context = {
            'registration_form': registration_form,
            'login_form': login_form
        }
        return render(request, 'account/registration.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'registration')
        if u_redirect is not None:
            return u_redirect

        login_form = forms.LoginForm(request.POST)
        registration_form = forms.RegistrationForm(request.POST)

        context = {
            'login_form': login_form,
            'registration_form': registration_form
        }

        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(
                username=data['user_login'],
                password=data['user_password']
            )
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Incorrect password')

        if registration_form.is_valid():
            data = registration_form.cleaned_data
            try:
                user = get_user_model().objects.create_user(
                    username=data['username'],
                    email=data['mail'],
                    password=data['password']
                )
                user.save()
                return redirect('main')
            except IntegrityError:
                messages.error(request, 'Пользователь с такими данными уже существует')

        return render(request, 'account/registration.html', context)


class ProfileView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request):
        user = request.user

        return render(request, 'account/profile.html')

    def post(self, request):
        u_redirect = email_and_search(request, 'profile')
        if u_redirect is not None:
            return u_redirect


class PasswordRecoveryView(View):
    def get(self, request):
        context = {}
        return render(request, 'account/recovery.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'recovery')
        if u_redirect is not None:
            return u_redirect

        username_to_pass = request.POST.get('username_for_pass')

        try:
            user = get_user_model().objects.get(username=username_to_pass)
        except get_user_model().DoesNotExist:
            messages.error(request, 'No such user')
            return render(request, 'account/recovery.html')

        email_to_pass = user.email

        try:
            code = VarificationCode.objects.get(user=user)
            code.delete()
        except VarificationCode.DoesNotExist:
            pass

        pass_key = VarificationCode(user=user, hash_key=hash_key(6), attempt_amount=0)
        pass_key.save()

        send_mail('bot', str(pass_key), 'glebabusya@mail.ru', [email_to_pass])

        return redirect('recovery_confirm', user)


class RecoveryConfirmView(View):

    def get(self, request, username):
        context = {'username': username}
        return render(request, 'account/recovery-confirm.html', context)

    def post(self, request, username):
        u_redirect = email_and_search(request, 'recovery_confirm')
        if u_redirect is not None:
            return u_redirect

        pass_key_confirm = request.POST.get('pass_key_confirm')
        user = get_user_model().objects.get(username=username)
        pass_key = VarificationCode.objects.get(user=user)

        if pass_key_confirm == pass_key:
            request.session['_username'] = username
            return redirect('password_change')

        if pass_key.attempt_amount > 2:
            pass_key.delete()
            messages.error(request, 'Too many attempts')
            return render(request, 'account/recovery.html', )

        pass_key.attempt_amount += 1
        pass_key.save()
        messages.error(request, 'Invalid code')

        return render(request, 'account/recovery-confirm.html', {'username': username})


class PasswordChangeView(View):

    def get(self, request):
        form = forms.ChangePasswordForm()
        username = request.session.get('_username')

        if username is None:
            return redirect('registration')

        context = {'form': form, 'username': username}

        return render(request, 'account/password-change.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'recovery_confirm')
        if u_redirect is not None:
            return u_redirect

        form = forms.ChangePasswordForm(request.POST)
        username = request.session.get('_username')

        context = {'form': form, 'username': username}
        if form.is_valid():
            new_password = form.cleaned_data['password']
            user = get_user_model().objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('registration')

        return render(request, 'account/password-change.html', context)