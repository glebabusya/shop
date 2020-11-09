from django import forms
from django.contrib.auth.models import User
from django.core import exceptions
from .models import ShopUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator


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


class LoginForm(forms.Form):
    user_login = forms.CharField(label='Username')
    user_password = forms.CharField(widget=forms.PasswordInput(), label='Password')


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), error_messages=None, label='New Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput(), error_messages=None)

    def clean(self):
        data = super().clean()
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise exceptions.ValidationError('Пароль введен неверно')


class ShopUserCreationForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'email')


class ShopUserChangeForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, required=False, widget=forms.EmailInput(attrs={'class': 'profile-input'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'profile-input image-input'}))
    phone_number = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'class': 'profile-input'}),
                                   validators=[
                                       # Регулярка для номера телефона
                                       RegexValidator(regex=r'\d{4}\w{2}-\d')])

    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'avatar', 'send_news']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'profile-input'}),
            'last_name': forms.TextInput(attrs={'class': 'profile-input'}),
            'send_news': forms.CheckboxInput(attrs={'class': 'profile-checkbox'})
        }
        labels = {
            'send_news': 'Subscribe me to Newsletter'
        }
