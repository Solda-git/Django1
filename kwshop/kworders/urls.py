from django.urls import path, include
import kworders.views as kworders


app_name = 'kworders'

urlpatterns = [
    path('', kworders.OrderList.as_view(), name='index'),
    path('create/', kworders.OrderCreate.as_view(), name='order_create'),
    path('update/<int:pk>', kworders.OrderUpdate.as_view(), name='order_update'),
    path('read/<int:pk>', kworders.OrderDetail.as_view(), name='order_read'),
    path('delete/<int:pk>', kworders.OrderDelete.as_view(), name='order_delete'),
]