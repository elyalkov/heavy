from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category
#render — функция, которая позволяет взять HTML-шаблон и вставить в него данные, а затем вернуть готовую HTML-страницу пользователю
#get_object_or_404 — функция, которая ищет объект в базе данных. Если объект не найден, она автоматически возвращает ошибку
def popular_list(request):
    products = Product.objects.filter(available=True)[:3]
    return render(request,
                  'main/index/index.html',
                  {'products': products}) #в словарь передаем значения, которые будем вызывать в html-шаблоне (for...in)


def product_detail(request, slug):
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    return render(request,
                  'main/product/detail.html',
                  {'product': product})


def product_list(request, category_slug=None):
    page= request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 10)
    current_page = paginator.page(int(page))
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        paginator = Paginator(products.filter(category=category), 10)
        #products = products.filter(category=category) удалили после добавления пагинатора
        current_page = paginator.page(int(page))
    return render(request,
                  'main/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': current_page, #products заменили на current_page после пагинатора
                   'slug_url': category_slug})