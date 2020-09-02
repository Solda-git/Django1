from django.db.models import ExpressionWrapper, F, DecimalField
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from cart.models import CartItem
from main.models import Product


def index(request):
    pass


def load_cart(user):
    return CartItem.objects.select_related().filter(user=user).annotate(
        cost=ExpressionWrapper(F('quantity')*F('product__price'), output_field=DecimalField())
    )

def add_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = CartItem.objects.filter(user=request.user, product=product).first()
    if not cart:
        cart = CartItem(user=request.user, product=product)
    cart.quantity += 1
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

