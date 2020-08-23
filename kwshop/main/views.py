from django.shortcuts import render


# Create your views here.

def index(request):
    context = {
        'page_title': 'Главная'
    }
    return render(request, 'main/index.html', context = context)

def catalog(request):
    context = {
        'page_title': 'Каталог'
    }
    return render(request, 'main/catalog.html', context = context)

def cart(request):
    context = {
        'page_title': 'Корзина'
    }
    return render(request, 'main/cart.html', context = context)

def contact(request):
    context = {
        'page_title': 'Обратная связь'
    }
    return render(request, 'main/contact.html', context = context)