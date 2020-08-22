from django.urls import path
from . import views

urlpatterns = [path('registration', views.RegLogView.as_view(), name='registration'),
               ]
