"""kwshop URL Configuration
    main application
"""

from django.urls import path
import cart.views as cart

app_name = 'kwauth'

urlpatterns = [
    path('', cart.index, name='index'),

]

