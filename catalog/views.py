from django.contrib.auth.models import AnonymousUser
from django.db import connection
from django.shortcuts import render, redirect
from django.views.generic import View

from account.models import FavoriteItem
from account.views.profile import adding_to_wishlist
from cart.views import adding_to_cart
from main.views import email_check, email_and_search, generate_context
from . import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages

ORDERING = {
    'Popularity': 'description',
    'Low - High Price': 'original_price',
    'High - Low Price': '-original_price',
    'Average Rating': 'id',
    'None': 'description'
}


class ItemView(View):
    def get(self, request, item_id):
        context = generate_context(request)

        item = models.Item.objects.get(id=item_id)
        context['item'] = item

        items = models.Item.objects.filter(featured=True)[:4]
        context['items'] = items

        context['marks'] = [5, 4, 3, 2, 1]

        comments = models.Comment.objects.filter(item=item)[:2]
        context['comments'] = comments

        return render(request, 'catalog/item.html', context)

    def post(self, request, item_id):
        u_redirect = email_and_search(request, 'item')
        if u_redirect is not None:
            return u_redirect

        add_to_wishlist = request.POST.get('wishlist') == 'To Wishist'

        amount_to_cart = request.POST.get('selection')

        if add_to_wishlist:
            if request.user.is_authenticated:
                adding_to_wishlist(user=request.user, item=models.Item.objects.get(id=item_id))
                messages.info(request, '<i class="fa fa-check-circle-o" aria-hidden="true"></i> Added to Wishlist')
            else:
                messages.error(request, '<i class="fa fa-ban" aria-hidden="true"></i> Login or Register')

        if isinstance(amount_to_cart, str):
            if request.user.is_authenticated:
                adding_to_cart(user=request.user, item=models.Item.objects.get(id=item_id), amount=int(amount_to_cart))

                messages.success(request, '<i class="fa fa-check-circle-o" aria-hidden="true"></i> Added to Cart')
            else:
                messages.error(request, '<i class="fa fa-ban" aria-hidden="true"></i> Login or Register')
        return redirect('item', item_id)


class CatalogView(View):
    def get(self, request, searching=None, order=None, page=1):
        context = generate_context(request)
        try:
            ordering = ORDERING[order]
        except KeyError:
            ordering = 'name'

        categories = models.Category.objects.all().order_by('name')
        context['categories'] = categories

        context['ordering'] = ordering

        context['searching'] = searching

        if searching is not None and searching != '' and searching != 'None':
            # Фильтрация и упорядочивание поиска
            filtered_items = list(models.Item.objects.filter(name__icontains=searching).order_by(ordering))
            categories_qs = models.Category.objects.filter(name__icontains=searching)
            brands_qs = models.Brand.objects.filter(name__icontains=searching)
            categories_items = list(models.Item.objects.filter(category__in=categories_qs).order_by(ordering))
            brands_items = list(models.Item.objects.filter(brand__in=brands_qs).order_by(ordering))
            for item in brands_items + categories_items:
                if item not in filtered_items:
                    filtered_items.append(item)
        else:
            filtered_items = models.Item.objects.filter(featured=True)

        paginator = Paginator(filtered_items, 12)

        try:
            items = paginator.page(page)
            context['items'] = items
            context['page'] = page
            context['next_page'] = page + 1
            context['previous_page'] = page - 1

        except PageNotAnInteger:
            items = paginator.page(1)
            context['items'] = items
            context['page'] = 1
            context['next_page'] = 2

        except EmptyPage:
            items = paginator.page(paginator.num_pages)
            context['items'] = items
            context['page'] = paginator.num_pages
            context['previous_page'] = paginator.num_pages - 1

        language = request.headers['Accept-Language'][:2]
        context['language'] = language

        return render(request, 'catalog/catalog.html', context)

    def post(self, request, searching=None, order=None, page=1):
        email_redirect = email_check(request, 'catalog', searching, order)
        if email_redirect is not None:
            return email_redirect

        search = request.POST.get('search')
        order = request.POST.get('selection')
        if search is not None and search != '':
            return redirect('catalog', search, order, 1)

        if order is not None:
            return redirect('catalog', searching, order, 1)

        return redirect('catalog')
