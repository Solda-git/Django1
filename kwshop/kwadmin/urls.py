"""kwshop URL Configuration
   admin application
"""

from django.urls import path
import kwadmin.views as kwadmin

app_name = 'kwadmin'

urlpatterns = [
    path('', kwadmin.index, name='index'),
]

