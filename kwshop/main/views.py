from django.shortcuts import render
from json import loads
from kwshop import settings
from main.models import ProductCat, Product

# Create your views here.

def index(request):
    products = loads(extract("catalog.JSON"))
    fixIMGURLs(products)
    cart = loads(extract("cart.JSON"))
    fixIMGURLs(cart)
    context = {
        'page_title': 'главная',
        'products': products,
        'cart': cart
    }
    return render(request, 'main/index.html', context = context)

def catalog(request):
    #from Lesson2 - to be deleted in the next branch
    # products = loads(extract("catalog.JSON"))
    # fixIMGURLs(products)

    # products load from DB
    products = Product.objects.all()
    categories = ProductCat.objects.all()

    # cart loads from JSON - to be refactored
    cart = loads(extract("cart.JSON"))
    fixIMGURLs(cart)
    context = {
        'page_title': 'каталог',
        'products': products,
        'cart': cart,
        'categories': categories,
    }
    return render(request, 'main/catalog.html', context = context)

def cart(request):
    products = Product.objects.all()
    categories = ProductCat.objects.all()
    cart = loads(extract("cart.JSON"))
    fixIMGURLs(cart)
    context = {
        'page_title': 'корзина',
        'cart': cart,
        'products': products,
        'categories': categories,
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
