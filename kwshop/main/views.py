from django.shortcuts import render


# Create your views here.

def index(request):
    print('From index.')
    return render(request, 'main/index.html')

def catalog(request):
    print('From catalog.')
    return render(request, 'main/catalog.html')

def cart(request):
    print('From cart.')
    return render(request, 'main/cart.html')

def contact(request):
    print('From contact.')
    return render(request, 'main/contact.html')