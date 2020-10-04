from django.urls import path, include

from . import views

urlpatterns = [path('', views.MainView.as_view(), name='main'),
               path('.<str:language>', views.MainView.as_view(), name='main'),

               path('catalog/', include('catalog.urls')),
               path('user/', include('account.urls'))
               ]
