"""kwshop URL Configuration
    main application
"""

from django.urls import path, re_path
import cart.views as cart

app_name = 'kwauth'

urlpatterns = [
    path('', cart.index, name='index'),
    re_path(r'^add/product/(?P<pk>\d+)/$', cart.add_item, name='add_item'),

]

