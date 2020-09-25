from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models

from kwshop import settings
from kwshop.settings import USER_EXPIRATION_PERIOD


def get_activation_key_expired():
    return now() + USER_EXPIRATION_PERIOD

class KWUser (AbstractUser):
    age = models.PositiveIntegerField(verbose_name='возраст', null=True)
    sex = models.CharField(verbose_name='пол', max_length=1, blank=True)
    avatar = models.ImageField(upload_to='users_ava', blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_activation_key_expired)


    def is_activation_key_expired(self):
        return  now() > self.activation_key_expires


    def cartItemsAmount(self):
        return sum(item.quantity for item in self.user_cart.all())

    def cartCost(self):
        return sum (item.product.price * item.quantity for item in self.user_cart.all ())

    def send_verify_mail(self):
        verify_link = reverse(
            'auth:user_verify',
            kwargs={
                'email': self.email,
                'activation_key': self.activation_key,
            }
        )
        title = f'Подтверждение для {self.username}'
        message = f'Для подтверждения учетоеной записи {self.username} на портале {settings.DOMAIN_NAME} '\
                  f'необходимо пройти по ссылке: \n {settings.DOMAIN_NAME}{verify_link}'
        return self.email_user(
            title,
            message,
            settings.EMAIL_HOST_USER,
            fail_silently=False
        )


    class Meta:
        # ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']
        ordering = ['is_active', '-is_superuser', '-is_staff', 'username']