from django.urls import path
from . import views

urlpatterns = [path('registration', views.RegLogView.as_view(), name='registration'),
               path('', views.ProfileView.as_view(), name='profile'),
               path('recovery', views.PasswordRecoveryView.as_view(), name='recovery'),
               path('recovery-confirm-<str:username>', views.RecoveryConfirmView.as_view(), name='recovery_confirm'),
               path('password-change', views.PasswordChangeView.as_view(), name='password_change')
               ]
