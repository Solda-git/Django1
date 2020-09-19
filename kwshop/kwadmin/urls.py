"""kwshop URL Configuration
   admin application
"""

from django.urls import path
import kwadmin.views as kwadmin

app_name = 'kwadmin'

urlpatterns = [
    # path ('', kwadmin.index, name='index'),
    path ('', kwadmin.UserList.as_view(), name='index'),
    path ('user/create/', kwadmin.user_create, name='user_create'),
    path ('user/<int:pk>/update/', kwadmin.user_update, name='user_update'),
    path ('user/<int:pk>/delete/', kwadmin.user_delete, name='user_delete'),

    path ('categories/', kwadmin.CategoryList.as_view(), name='category_list'),
    path ('categories/create/', kwadmin.CategoryCreate.as_view(), name='category_create'),
    path ('category/<int:cat_pk>/update/', kwadmin.CategoryUpdate.as_view(), name='category_update'),
    path ('category/<int:cat_pk>/delete/', kwadmin.CategoryDelete.as_view(), name='category_delete'),

    path ('category/<int:cat_pk>/products/', kwadmin.category_products, name='category_products'),
    path ('category/<int:cat_pk>/product/create/', kwadmin.product_create, name='product_create'),
    path ('product/<int:pk>/update/', kwadmin.product_update, name='product_update'),
    path ('product/<int:pk>/delete/', kwadmin.product_delete, name='product_delete'),
]
