from django.contrib.auth import get_user_model
from django.db import models
from main.models import Product


# class CartQuerySet(models.QuerySet):
        # def delete(self):
        #     for object in self:
        #         object.product.quantity += object.quantity
        #         object.product.save()
        #     super().delete()

class CartItem (models.Model):
    # objects = CartQuerySet.as_manager()
    user = models.ForeignKey (
        get_user_model (),
        on_delete=models.CASCADE,
        related_name='user_cart'
    )
    product = models.ForeignKey (Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField (default=0)
    time_added = models.DateTimeField (auto_now_add=True)

    # def delete(self, using=None, keep_parent=False):
    #     self.product.quantity += self.total_quantity
    #     self.product.save()
    #     super.delete(using=None, keep_parent=False)
    #

    @classmethod
    def get_item(cls, pk):
        return cls.objects.filter(pk=pk).first()

