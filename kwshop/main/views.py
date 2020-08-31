from django.shortcuts import render, get_object_or_404
from json import loads
from kwshop import settings
from main.models import ProductCat, Product

# Create your views here.

def get_menu2():
    return ProductCat.objects.all()

def index(request):

    # products load from DB
    products = Product.objects.all()

    cart = loads(extract("cart.JSON"))
    fixIMGURLs(cart)
    context = {
        'page_title': 'главная',
        'products': products,
        'categories': get_menu2(),
        'cart': cart
    }
    return render(request, 'main/index.html', context=context)

def catalog(request):

    products = Product.objects.all()

    # cart loads from JSON - to be refactored
    cart = loads(extract("cart.JSON"))
    fixIMGURLs(cart)
    context = {
        'page_title': 'каталог',
        'products': products,
        'cart': cart,
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

    context = {
        'page_title': 'каталог',
        'categories': get_menu2(),
        'category': cat,
        'products': products,
    }
    return render(request, 'main/catalog.html', context=context)

def cart(request):
    products = Product.objects.all()
    cart = loads(extract("cart.JSON"))
    fixIMGURLs(cart)
    context = {
        'page_title': 'корзина',
        'cart': cart,
        'products': products,
        'categories': get_menu2(),
    }
    return render(request, 'main/cart.html', context = context)

def contact(request):
    cart = loads(extract("cart.JSON"))
    fixIMGURLs(cart)
    context = {
        'page_title': 'обратная связь',
        'cart': cart
    }
    return render(request, 'main/contact.html', context = context)

#####################################################################
def extract(filename):
    """
    temporary function for working with JSON files while database access is not applied
    :param filename: name of JSON file placed in 'BASE_DIR\main\JSON' directory
    :return: JSON string to be parsed
    """
    handle = open(settings.BASE_DIR + "\main\JSON\\" + filename, "r", encoding="utf-8")
    JSONbuffer = ''
    for string in handle:
        JSONbuffer += string
    handle.close
    return JSONbuffer

def fixIMGURLs(obj):
    """
    adding dynamic behavior in static ursl from JSON
    'obj' dictionary has to contain key item "img"
    :param obj: JSON-generated object to be fixed
    :return:
    """
    for item in obj:
        item["img"] = settings.STATIC_URL + item["img"]
