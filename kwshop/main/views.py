from django.shortcuts import render


# Create your views here.

def index(request):
    context = {
        'page_title': 'главная'
    }
    return render(request, 'main/index.html', context = context)

def catalog(request):
    context = {
        'page_title': 'каталог'
    }
    return render(request, 'main/catalog.html', context = context)

def cart(request):
    context = {
        'page_title': 'корзина'
    }
    return render(request, 'main/cart.html', context = context)

def contact(request):
    context = {
        'page_title': 'обратная связь'
    }
    return render(request, 'main/contact.html', context = context)