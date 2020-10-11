from django.core.cache import cache

from kwshop import settings
from main.models import ProductCat

#
# def catalog_menu(request):
#     if settings.LOW_CACHE:
#         key = 'links_menu'
#         links_menu = cache.get(key)
#         if links_menu is None:
#             links_menu = ProductCat.objects.filter(is_active=True)
#             cache.set(key, links_menu)
#     else:
#         links_menu = ProductCat.objects.filter(is_active=True)
#     return {
#         'catalog_menu': links_menu,
#     }



def catalog_menu(request):
    return {
        'catalog_menu': ProductCat.objects.filter(is_active=True),
    }