import random

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from json import loads

from django.views.decorators.cache import cache_page

from cart.views import load_cart
from kwshop import settings
from kwshop.settings import PRODUCTS_ON_PAGE_NUMBER
from main.models import ProductCat, Product


#
# def get_menu2():
#     return ProductCat.objects.all()


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.select_related('category').filter(is_active=True, category__is_active=True)
            cache.set(key, products)
        return products
    else:
        return Product.objects.select_related('category').filter(is_active=True, category__is_active=True)



def get_hot_product():
    return random.choice(get_products())


def index(request):
    page = 1
    cart_items= None
    products = get_products()
    if request.user.is_authenticated:
        cart_items= load_cart(request.user)

    #################
    paginator = Paginator(products, PRODUCTS_ON_PAGE_NUMBER)
    try:
        product_paginator = paginator.page(page)
    except PageNotAnInteger:
        product_paginator = paginator.page(1)
    except EmptyPage:
        product_paginator = paginator.page(paginator.num_pages)
    #################

    context = {
        'page_title': 'главная',
        'products': product_paginator,
        # 'categories': get_menu2(),
        'cart': cart_items,
    }
    return render(request, 'main/index.html', context=context)


# @cache_page(3600)
def catalog(request, page=1):
    cart_items= None
    products = get_products()
    if request.user.is_authenticated:
        cart_items= load_cart(request.user)

    #################
    paginator = Paginator(products, PRODUCTS_ON_PAGE_NUMBER)
    try:
        product_paginator = paginator.page(page)
    except PageNotAnInteger:
        product_paginator = paginator.page(1)
    except EmptyPage:
        product_paginator = paginator.page(paginator.num_pages)
    #################

    context = {
        'page_title': 'каталог',
        'products': product_paginator,
        'cart': cart_items,
        # 'categories': get_menu2(),
        'category': {'pk': 0},
        'hot_product': get_hot_product(),
    }
    return render(request, 'main/catalog.html', context=context)


def category(request, pk=0, page=1):
    print(pk)
    cart_items = None
    if int(pk) == 0:
        products = get_products()
        cat = {
            'pk': 0,
        }
    else:
        cat = get_object_or_404(ProductCat, pk=int(pk))
        products = Product.objects.filter(category=cat, is_active=True)
    if request.user.is_authenticated:
        cart_items= load_cart(request.user)
    paginator = Paginator(products, 4)
    try:
        product_paginator = paginator.page(int(page))
    except PageNotAnInteger:
        product_paginator = paginator.page(0)
    except EmptyPage:
        product_paginator = paginator.page(paginator.num_pages)
    context = {
        'page_title': 'каталог',
        'category': cat,
        'products': product_paginator,
        'cart': cart_items,
        'hot_product': get_hot_product(),
    }
    return render(request, 'main/catalog.html', context=context)


@login_required
def cart(request):
    products = get_products()
    cart_items = load_cart(request.user)
    context = {
        'page_title': 'корзина',
        'cart': cart_items,
        'products': products,
        # 'categories': get_menu2(),
    }
    return render(request, 'main/cart.html', context=context)


def contact(request):
    cart_items = None
    if request.user.is_authenticated:
        cart_items = load_cart(request.user)
    context = {
        'page_title': 'обратная связь',
        'cart': cart_items,
    }
    return render(request, 'main/contact.html', context=context)


def product(request, pk):
    cart_items = None
    if request.user.is_authenticated:
        cart_items = load_cart(request.user)
    productItem = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': productItem.name,
        'cart': cart_items,
        'product': productItem,
    }
    return render(request, 'main/product.html', context=context)


def product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
        return JsonResponse({"price": product and product.price or 0})
