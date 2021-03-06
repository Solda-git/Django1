from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property

from main.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'
    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(
        verbose_name='статус',
        max_length=3 ,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING
    )
    is_active = models.BooleanField(verbose_name='активен', default=True, db_index=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    @property
    def is_forming(self):
        return self.status == self.FORMING

    @cached_property
    def order_items(self):
        return self.orderitems.select_related().all()

    @cached_property
    def total_quantity(self):
        return sum(list(map(lambda x: x.quantity, self.order_items)))

    # def get_product_type_quantity(self):
    #     items = self.orderitems.select_related()
    #     return len(items)
    #
    @cached_property
    def total_cost(self):
        return sum(list(map(lambda x: x.quantity * x.product.price, self.order_items)))
# переопределяем метод, удаляющий объект


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    @cached_property
    def product_cost(self):
        return self.product.price * self.quantity

    # def delete(self, using=None, keep_parent=False):
    #     self.product.quantity += self.total_quantity
    #     self.product.save()
    #     super.delete(using=None, keep_parent=False)

    @classmethod
    def get_item(cls, pk):
        return cls.objects.filter(pk=pk).first()