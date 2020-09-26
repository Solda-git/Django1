from django.urls import path, include
import kworders.views as kworders


app_name = 'kworders'

urlpatterns = [
    path('', kworders.index, name='index'),


]