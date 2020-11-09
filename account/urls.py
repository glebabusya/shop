from django.urls import path, include
from .views import registration, profile

urlpatterns = [path('registration', registration.RegLogView.as_view(), name='registration'),
               path('recovery', registration.PasswordRecoveryView.as_view(), name='recovery'),
               path('recovery-confirm-<str:username>', registration.RecoveryConfirmView.as_view(),
                    name='recovery_confirm'),
               path('password-change', registration.PasswordChangeView.as_view(), name='password_change'),

               path('orders', profile.OrdersView.as_view(), name='orders'),
               path('profile', profile.ProfileView.as_view(), name='profile'),
               path('wishlist', profile.WishListView.as_view(), name='wishlist')
               ]
