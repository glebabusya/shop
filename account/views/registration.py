import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import View
from main.views import email_and_search, generate_context
from .. import forms
from ..models import VarificationCode
from django.contrib.auth import logout


def hash_key(amount):
    """function of generating key to restore the password"""
    result = ''
    variants = 'abcdefghjklmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ0123456789'
    for symbol in range(amount):
        result += random.choice(variants)
    return result


class RegLogView(View):
    def get(self, request):
        logout(request)
        context = generate_context(request)

        registration_form = forms.RegistrationForm()
        login_form = forms.LoginForm()

        context['registration_form'] = registration_form
        context['login_form'] = login_form

        return render(request, 'account/registration.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'registration')
        if u_redirect is not None:
            return u_redirect

        context = generate_context(request)

        login_form = forms.LoginForm(request.POST)
        registration_form = forms.RegistrationForm(request.POST)

        context['registration_form'] = registration_form
        context['login_form'] = login_form

        if login_form.is_valid():  # login
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

        if registration_form.is_valid():  # registration
            data = registration_form.cleaned_data
            try:
                user = get_user_model().objects.create_user(
                    username=data['username'],
                    email=data['mail'],
                    password=data['password']
                )
                user.save()
                return redirect('profile')
            except IntegrityError:
                messages.error(request, 'Пользователь с такими данными уже существует')

        return render(request, 'account/registration.html', context)


class PasswordRecoveryView(View):
    def get(self, request):
        context = generate_context(request)
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

        try:
            code = VarificationCode.objects.get(user=user)
            code.delete()
        except VarificationCode.DoesNotExist:
            pass

        pass_key = VarificationCode(user=user, hash_key=hash_key(6), attempt_amount=0)
        pass_key.save()

        send_mail('bot', str(pass_key), 'glebabusya@mail.ru', [user.email])

        return redirect('recovery_confirm', user)


class RecoveryConfirmView(View):

    def get(self, request, username):
        context = generate_context(request)
        context['username'] = username
        return render(request, 'account/recovery-confirm.html', context)

    def post(self, request, username):
        u_redirect = email_and_search(request, 'recovery_confirm')
        if u_redirect is not None:
            return u_redirect

        context = generate_context(request)

        pass_key_confirm = request.POST.get('pass_key_confirm')
        user = get_user_model().objects.get(username=username)
        pass_key = VarificationCode.objects.get(user=user)

        context['username'] = username

        if pass_key_confirm == str(pass_key):
            request.session['_username'] = username
            return redirect('password_change')

        if pass_key.attempt_amount > 2:
            pass_key.delete()
            messages.error(request, 'Too many attempts')
            return redirect('recovery')

        pass_key.attempt_amount += 1
        pass_key.save()
        messages.error(request, 'Invalid code')

        return render(request, 'account/recovery-confirm.html', context)


class PasswordChangeView(View):

    def get(self, request):
        context = generate_context(request)

        form = forms.ChangePasswordForm()
        username = request.session.get('_username')

        if username is None:
            return redirect('registration')

        context['form'] = form
        context['username'] = username

        return render(request, 'account/password-change.html', context)

    def post(self, request):
        u_redirect = email_and_search(request, 'recovery_confirm')
        if u_redirect is not None:
            return u_redirect

        context = generate_context(request)

        form = forms.ChangePasswordForm(request.POST)
        username = request.session.get('_username')

        context['form'] = form
        context['username'] = username

        if form.is_valid():
            new_password = form.cleaned_data['password']
            user = get_user_model().objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('registration')

        return render(request, 'account/password-change.html', context)
