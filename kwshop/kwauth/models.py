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

class KWUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOISES = (
        (MALE, 'M'),
        (FEMALE, 'F'),
    )

    user = models.OneToOneField(KWUser, primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOISES, blank=True)

