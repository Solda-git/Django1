from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from kworders.forms import OrderForm, OrderItemForm
from kworders.models import Order, OrderItem


class OrderList(ListView):
    model = Order


class OrderCreate (CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data (self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra= 1
        )
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            cart_items = self.request.user.user_cart.all()
            if cart_items and len(cart_items):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=len(cart_items)
                )
                formset = OrderFormSet()
                for form, cart_item  in zip(formset.forms, cart_items):
                    form.initial['product'] = cart_item.product
                    form.initial['quantity'] = cart_item.quantity
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def  form_valid (self, form):
        context = self.get_context_data()
        orderitems = context[ 'orderitems' ]

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
# удаляем пустой заказ
#         if self.object.get_total_cost() ==  0  :
            self.request.user.user_cart.all().delete()
        return super().form_valid(form)


class OrderUpdate (UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data (self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra= 1
        )
        if self.request.POST:
            formset = OrderFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            formset = OrderFormSet(instance=self.object)
        data['orderitems'] = formset
        return data

    def  form_valid (self, form):
        context = self.get_context_data()
        orderitems = context[ 'orderitems' ]

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
# удаляем пустой заказ
#         if self.object.get_total_cost() ==  0  :
#             self.reqest.user.user_cart.all().delete()
        return super().form_valid(form)
