"""kwshop URL Configuration
    main application
"""

from django.urls import path, re_path
import cart.views as cart

app_name = 'cart'

urlpatterns = [
    path ('', cart.index, name='index'),
    re_path (r'^add/product/(?P<pk>\d+)/$', cart.add_item, name='add_item'),
    re_path (r'^delete/cart/items/(?P<pk>\d+)/$', cart.delete_items, name='del_items'),
    re_path (r'^delete/cart/items/(?P<pk>\d+)/$', cart.delete_items, name='del_items'),
    path ('change/<int:pk>/quantity/<int:quantity>/', cart.edit_items, name='edit_items'),
]
