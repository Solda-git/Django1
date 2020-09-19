from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class KWUser (AbstractUser):
    age = models.PositiveIntegerField(verbose_name='возраст', null=True)
    sex = models.CharField(verbose_name='пол', max_length=1, blank=True)
    avatar = models.ImageField(upload_to='users_ava', blank=True)

    def cartItemsAmount(self):
        return sum(item.quantity for item in self.user_cart.all())

    def cartCost(self):
        return sum (item.product.price * item.quantity for item in self.user_cart.all ())

    class Meta:
        # ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']
        ordering = ['is_active', '-is_superuser', '-is_staff', 'username']