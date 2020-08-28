# -*- coding utf-8 -*-
import os, json

from django.core.management.base import BaseCommand

from kwauth.models import KWUser
from kwshop.settings import JSON_PATH
from main.models import Product, ProductCat
from django.conf import settings


def load_table(file):
    with open(
            os.path.join(JSON_PATH, f'{file}.json'),
            encoding='utf-8'
    ) as file_handler:
        return json.load(file_handler)


class Command(BaseCommand):
    help = 'Fill DB from catalog JSON'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        ProductCat.objects.all().delete()

        categories = load_table('categories')
        for category in categories:
            ProductCat.objects.create(**category)

        products = load_table('products')
        for product in products:
            product["category"] = ProductCat.objects.get(title=product["category"])
            Product.objects.create(**product)

        if not KWUser.objects.filter(username='django').exists():
            KWUser.objects.create_superuser(username='django', email='', password='geekbrains')
