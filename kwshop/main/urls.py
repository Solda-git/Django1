"""kwshop URL Configuration
    main application
"""

from django.urls import path
import main.views as main

app_name = 'main'

urlpatterns = [
    path('', main.index, name='index'),
    path('catalog/', main.catalog, name='catalog'),
    path('category/<int:pk>/', main.category, name='category'),
    path('cart/', main.cart, name='cart'),
    path('contact/', main.contact, name='contact'),
    path('product/<int:pk>/', main.product, name='product'),

]

