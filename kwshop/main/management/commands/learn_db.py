# -*- coding utf-8 -*-
import os, json
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q, F, When, Case, IntegerField, DecimalField

from kwauth.models import KWUser
from kworders.models import OrderItem
from kwshop.settings import JSON_PATH
from main.models import Product, ProductCat
from django.conf import settings



class Command(BaseCommand):
    help = 'This command fills prints the profit values of the marketing company of kwshop.'

    def handle(self, *args, **kwargs):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)
        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & Q(order__updated__lte=F('order__created') + action_2__time_delta)
        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__total_discount = When(action_1__condition, then=F('product__price') * F('quantity') * action_1__discount)

        action_2__total_discount = When(action_2__condition, then=F('product__price') * F('quantity') * -action_2__discount)

        action_expired__total_discount = When(action_expired__condition, then=F('product__price') * F('quantity') * action_expired__discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_discount=Case(
                action_1__total_discount,
                action_2__total_discount,
                action_expired__total_discount,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_discount').select_related()

        for orderitem in test_orders:
            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}:'
                  f'{orderitem.product.name:15}: скидка {abs(orderitem.total_discount):6.2f} руб. |  '
                  f'{orderitem.order.updated - orderitem.order.created}')
