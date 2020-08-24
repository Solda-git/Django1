from django.db import models

# Create your models here.
class Product(models.Model):
    pass

class ProductCat(models.Model):
    title = models.CharField(max_length=25, verbose_name='Категория')


