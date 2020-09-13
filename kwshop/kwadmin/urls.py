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
]
