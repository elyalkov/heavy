from django.shortcuts import render, get_object_or_404
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

