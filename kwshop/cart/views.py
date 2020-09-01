from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from cart.models import CartItem
from main.models import Product


def index(request):
    pass

def add_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = CartItem.objects.filter(user=request.user, product=product).first()
    if not cart:
        cart = CartItem(user=request.user, product=product)
    cart.quantity += 1
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
