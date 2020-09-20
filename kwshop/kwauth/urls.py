"""kwshop URL Configuration
    authentication application
"""

from django.urls import path
import kwauth.views as kwauth

app_name = 'kwauth'

urlpatterns = [
    path('login/', kwauth.login, name='login'),
    path('logout/', kwauth.logout, name='logout'),
    path('register/', kwauth.register, name='register'),
    path('profile/', kwauth.profile, name='profile'),
    path('user/verify/<str:email>/<str:activation_key>', kwauth.user_verify, name='user_verify'),
    path('user/alert/<str:email>/', kwauth.UserInform.as_view(), name='user_alert')

]

