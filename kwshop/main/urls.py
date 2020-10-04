"""kwshop URL Configuration
    main application
"""

from django.urls import path
import main.views as main

app_name = 'main'

urlpatterns = [
    path('', main.index, name='index'),
    path('catalog/', main.catalog, name='catalog'),

    path('catalog/products/page/<int:page>', main.catalog, name='catalog_all_page'),

    path('category/<int:pk>/', main.category, name='category'),
    path('category/<int:pk>/products/page/<int:page>', main.category, name='catalog_page'),
    path('cart/', main.cart, name='cart'),
    path('contact/', main.contact, name='contact'),
    path('product/<int:pk>/', main.product, name='product'),

    path('product/<int:pk>/price/', main.product_price),
]

