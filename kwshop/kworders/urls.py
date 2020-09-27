from django.urls import path, include
import kworders.views as kworders


app_name = 'kworders'

urlpatterns = [
    path('', kworders.OrderList.as_view(), name='index'),
    path('create/', kworders.OrderCreate.as_view(), name='order_create'),
    path('update/<int:pk>', kworders.OrderUpdate.as_view(), name='order_update'),
]