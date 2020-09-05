from django.contrib.auth import get_user_model
from django.db import models
from main.models import Product


class CartItem (models.Model):
    user = models.ForeignKey (
        get_user_model (),
        on_delete=models.CASCADE,
        related_name='user_cart'
    )
    product = models.ForeignKey (Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField (default=0)
    time_added = models.DateTimeField (auto_now_add=True)

