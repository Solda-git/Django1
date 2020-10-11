from django.contrib.auth.decorators import login_required
from django.db.models import ExpressionWrapper, F, DecimalField
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from cart.models import CartItem
from kworders.models import OrderItem
from main.models import Product


def index(request):
    pass


def load_cart(user):
    return user.user_cart.select_related('product', 'product__category').all().annotate(
        cost=ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField())
    )


@login_required
def add_item(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse(
                'main:product',
                kwargs={'pk': pk}
            )
        )
    product = get_object_or_404(Product, pk=pk)
    cart = CartItem.objects.filter(user=request.user, product=product).first()
    if not cart:
        cart = CartItem(user=request.user, product=product)
    cart.quantity += 1
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_items(request, pk, quantity):
    if request.is_ajax():
        item = CartItem.objects.get(pk=pk)
        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
        cart = load_cart(request.user)
        context = {
            'cart': cart,
            'cart_cost': request.user.cart_items_amount(),
            'cart_quantity': request.user.cart_cost(),
        }
        data = render_to_string('main/includes/inc__cart_body.html', context=context, request=request)
        return HttpResponse(data)


@login_required
def delete_items(request, pk):
    get_object_or_404(CartItem, pk=int(pk)).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def delete(self):
        self.product.quantity += self.total_quantity
        self.product.save()
        super.delete(using=None, keep_parent=False)


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=CartItem)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    print(type(sender), 'pre_save')
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=CartItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    print(type(sender), 'pre_delete')
    instance.product.quantity += instance.quantity
    instance.product.save()
