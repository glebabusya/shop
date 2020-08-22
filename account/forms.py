from django import forms
from django.core import exceptions
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(error_messages=None)
    mail = forms.EmailField(error_messages=None, )
    password = forms.CharField(widget=forms.PasswordInput(), error_messages=None)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), error_messages=None)

    def clean(self):
        data = super().clean()
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise exceptions.ValidationError('Пароль введен неверно')
        users = User.objects.all()
        mail = data.get('mail')
        for user in users:
            if mail == user.email:
                raise exceptions.ValidationError('Такая почта уже занята')


class LoginForm(forms.Form):
    user_login = forms.CharField(label='Username')
    user_password = forms.CharField(widget=forms.PasswordInput(), label='Password')
