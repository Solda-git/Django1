from django.shortcuts import render, get_object_or_404
from json import loads

from cart.views import load_cart
from kwshop import settings
from main.models import ProductCat, Product

# Create your views here.

def get_menu2():
    return ProductCat.objects.all()

def index(request):

    products = Product.objects.all()
    cartItems = load_cart(request.user)["cartItems"]

    context = {
        'page_title': 'главная',
        'products': products,
        'categories': get_menu2(),
        'cart': cartItems,
    }
    return render(request, 'main/index.html', context=context)

def catalog(request):

    products = Product.objects.all()

    cartItems = load_cart(request.user)["cartItems"]
    context = {
        'page_title': 'каталог',
        'products': products,
        'cart': cartItems,
        'categories': get_menu2(),
    }
    return render(request, 'main/catalog.html', context=context)

def category(request, pk):
    if pk == 0:
        products = Product.objects.all()
        cat = 0
    else:
        cat = get_object_or_404(ProductCat, pk=pk)
        products = Product.objects.filter(category=cat)
    cartItems = load_cart (request.user)["cartItems"]
    context = {
        'page_title': 'каталог',
        'categories': get_menu2(),
        'category': cat,
        'products': products,
        'cart': cartItems,
    }
    return render(request, 'main/catalog.html', context=context)

def cart(request):
    products = Product.objects.all()
    cart_items = load_cart(request.user)["cartItems"]
    cart_amount = load_cart(request.user)["cartItemsAmount"]
    cart_cost = load_cart(request.user)["cartCost"]

    context = {
        'page_title': 'корзина',
        'cart': cart_items,
        'cost': cart_amount,
        'amount': cart_cost,
        'products': products,
        'categories': get_menu2(),
    }
    return render(request, 'main/cart.html', context=context)

def contact(request):
    # cartItems = loads(extract("cart.JSON"))
    # fixIMGURLs(cartItems)

    cart_items = load_cart(request.user)["cartItems"]
    context = {
        'page_title': 'обратная связь',
        'cart': cart_items,
    }
    return render(request, 'main/contact.html', context=context)
