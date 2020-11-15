from django.urls import path

from . import views

urlpatterns = [
    path('item/<int:item_id>', views.ItemView.as_view(), name='item'),
    path('item/<int:item_id>/comments', views.CommentView.as_view(), name='comments'),

    path('', views.CatalogView.as_view(), name='catalog'),
    path('search=<str:searching>', views.CatalogView.as_view(), name='catalog'),
    path('search=<str:searching>/order=<str:order>', views.CatalogView.as_view(), name='catalog'),
    path('page=<int:page>', views.CatalogView.as_view(), name='catalog'),
    path('search=<str:searching>/page=<int:page>', views.CatalogView.as_view(), name='catalog'),
    path('search=<str:searching>/order=<str:order>/page=<int:page>', views.CatalogView.as_view(),
         name='catalog'),
]
