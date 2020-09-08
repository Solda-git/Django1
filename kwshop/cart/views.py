from django.contrib.auth.decorators import login_required
from django.db.models import ExpressionWrapper, F, DecimalField
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from cart.models import CartItem
from main.models import Product


def index(request):
    pass


def load_cart(user):
    return user.user_cart.all ().annotate (
        cost=ExpressionWrapper (F ('quantity') * F ('product__price'), output_field=DecimalField ())
    )



@login_required
def add_item(request, pk):

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect (
            reverse (
                'main:product',
                kwargs={'pk': pk}
            )
        )
    product = get_object_or_404 (Product, pk=pk)
    cart = CartItem.objects.filter (user=request.user, product=product).first ()
    if not cart:
        cart = CartItem (user=request.user, product=product)
    cart.quantity += 1
    cart.save ()
    return HttpResponseRedirect (request.META.get ('HTTP_REFERER'))


# def delete_item(request, cartitem_pk):  # decrement - to be added further
#     pass

@login_required
def edit_items(request, pk, quantity):
    print('is_ajax:', request.is_ajax())
    if request.is_ajax():
        item = CartItem.objects.get(pk=pk)

        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        cart = load_cart()

        data = {
            'cart': cart,
            'cart_cost': request.user.cartItemsAmounts(),
            'cart_quantity': request.user.cartCost(),
        }
        return JsonResponse (data)



@login_required
def delete_items(request, pk):
    get_object_or_404 (CartItem, pk=int (pk)).delete ()
    return HttpResponseRedirect (request.META.get ('HTTP_REFERER'))
