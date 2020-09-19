from django.db import models


class ProductCat(models.Model):
    title = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}({self.description})'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(ProductCat,
                                 on_delete=models.PROTECT,
                                 verbose_name='Категория')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2, default=0)
    img = models.ImageField(upload_to='product_imgs', blank=True)
    size = models.CharField(max_length=50, verbose_name='Размер', default='см')
    stuff = models.CharField(max_length=100, verbose_name='Материал', default='акриловые нитки, холофайбер')
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField (default=True)

    def __str__(self):
        return f'{self.name}, категория: {self.category.title}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

