from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class KWUser (AbstractUser):
    age = models.PositiveIntegerField(verbose_name='возраст', null=True)
    avatar = models.ImageField(upload_to='users_ava', blank=True)