"""kwshop URL Configuration
    main application
"""

from django.urls import path
import kwauth.views as kwauth

app_name = 'kwauth'

urlpatterns = [
    path('login/', kwauth.login, name='login'),
    path('logout/', kwauth.logout, name='logout'),
    path('register/', kwauth.register, name='register'),
    path('profile/', kwauth.profile, name='profile'),
]

