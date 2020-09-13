"""kwshop URL Configuration
   admin application
"""

from django.urls import path
import kwadmin.views as kwadmin

app_name = 'kwadmin'

urlpatterns = [
    path('', kwadmin.index, name='index'),
    path('user/create/', kwadmin.user_create, name='user_create'),
    path('user/<int:pk>/update/', kwadmin.user_update, name='user_update'),
]

