from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from kworders.forms import OrderForm, OrderItemForm
from kworders.models import Order, OrderItem


class LoggedUserCheckMixin:
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class TitleMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.user.username
        return context


class OrderList(TitleMixin, LoggedUserCheckMixin, ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(TitleMixin, LoggedUserCheckMixin, CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            cart_items = self.request.user.user_cart.select_related().all()
            if cart_items and len(cart_items):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=len(cart_items)
                )
                formset = OrderFormSet()
                for form, cart_item in zip(formset.forms, cart_items):
                    form.initial['product'] = cart_item.product
                    form.initial['quantity'] = cart_item.quantity
                    form.initial['price'] = cart_item.product.price
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

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


class OrderUpdate(TitleMixin, LoggedUserCheckMixin, UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )
        if self.request.POST:
            formset = OrderFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        # удаляем пустой заказ
        #         if self.object.get_total_cost() ==  0  :
        #             self.reqest.user.user_cart.all().delete()
        return super().form_valid(form)


class OrderDetail(TitleMixin, LoggedUserCheckMixin, DetailView):
    model = Order


class OrderDelete(TitleMixin, LoggedUserCheckMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders:index')

@login_required()
def order_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:index'))
