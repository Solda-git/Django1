from django.contrib.auth.decorators import login_required
from django.db.models import ExpressionWrapper, F, DecimalField
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from cart.models import CartItem
from main.models import Product


def index(request):
    pass

def load_cart(user):
    # cartItems = CartItem.objects.select_related().filter(user=user).annotate(
    #     cost=ExpressionWrapper(F('quantity')*F('product__price'), output_field=DecimalField())
    # )
    cartItems = user.cart.all().annotate(
        cost=ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField())
    )

    amount = cost = 0
    for item in cartItems:
        amount += item.quantity
        cost += item.cost
    cart = {
        'cartItems': cartItems,
        'cartItemsAmount': amount,
        'cartCost': cost,
    }
    return cart

@login_required
def add_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = CartItem.objects.filter(user=request.user, product=product).first()
    if not cart:
        cart = CartItem(user=request.user, product=product)
    cart.quantity += 1
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
