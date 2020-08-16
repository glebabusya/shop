from django.shortcuts import render, redirect
from django.views.generic import View
from main.views import email_check
from . import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

ORDERING = {
    'Popularity': 'description',
    'Low - High Price': 'original_price',
    'High - Low Price': '-original_price',
    'Average Rating': 'id',
    'None': 'description'
}


class ItemView(View):
    def get(self, request, item_id):
        item = models.Item.objects.get(id=item_id)
        categories = models.Category.objects.all()
        items = models.Item.objects.filter(featured=True)[:4]
        context = {'item': item,
                   'categories': categories,
                   'marks': [5, 4, 3, 2, 1],
                   'items': items
                   }
        comments = models.Comment.objects.filter(item=item)
        context['comments'] = comments[:2]
        return render(request, 'catalog/item.html', context)

    def post(self, request, item_id):
        email_check(request.POST.get('mail'), 'item', item_id)
        search = request.POST.get('search')
        if search is not None and search != '':
            return redirect('catalog', search)
        return redirect('item', item_id)


class CatalogView(View):
    def get(self, request, searching=None, order=None, page=1):

        try:
            ordering = ORDERING[order]
        except KeyError:
            ordering = 'name'

        categories = models.Category.objects.all().order_by('name')

        context = {
            'ordering': ordering,
            'categories': categories,
            'searching': searching,
        }

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
        email_check(request.POST.get('mail'), 'catalog', searching, order)

        search = request.POST.get('search')
        order = request.POST.get('selection')
        if search is not None and search != '':
            return redirect('catalog', search, order, 1)

        if order is not None:
            return redirect('catalog', searching, order, 1)

        return redirect('catalog')
