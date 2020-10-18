from django.core.management import call_command
from django.test import TestCase, Client


# Create your tests here.
from django.urls import reverse

from kwauth.models import KWUser
from main.models import ProductCat, Product


class TestMainSmoke(TestCase):
    # fixtures = ['kwauth.json', 'main.json', 'cart.json', 'orders.json']
    fixtures = ['main.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    # def setUp(self):
    #     self.client = Client()

        # self.superuser = KWUser.objects.create_superuser('django2', \
        #                                                   'django2@geekshop.local', 'geekbrains')
        #
        # self.user = KWUser.objects.create_user('tarantino', \
        #                                         'tarantino@geekshop.local', 'geekbrains')
        #
        # self.user_with__first_name = KWUser.objects.create_user('umaturman', \
        #                                                          'umaturman@geekshop.local', 'geekbrains', first_name='Ума')

    def test_main_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('main:contact'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('main:catalog'))
        self.assertEqual(response.status_code, 200)



    def test_product_cat_urls(self):

        response = self.client.get('/category/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('main:category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        for category in ProductCat.objects.all():
            response = self.client.get(reverse('main:category', kwargs={'pk': category.pk}))
            self.assertEqual(response.status_code, 200)

    def test_product_urls(self):
        for product in Product.objects.all():
            response = self.client.get(reverse('main:product', kwargs={'pk': product.pk}))
            self.assertEqual(response.status_code, 200)

# def test_user_login(self):
#     # главная без логина
#     response = self.client.get('/')
#     self.assertEqual(response.status_code, 200)
#     self.assertTrue(response.context['user'].is_anonymous)
#     self.assertEqual(response.context['title'], 'главная')
#     self.assertNotContains(response, 'Пользователь', status_code=200)
#
#     self.client.login(username='tarantino', password='geekbrains')
#
#     # логинимся
#     response = self.client.get('/auth/login/')
#     self.assertFalse(response.context['user'].is_anonymous)
#     self.assertEqual(response.context['user'], self.user)
#
#     # главная после логина
#     response = self.client.get('/')
#     self.assertContains(response, 'Пользователь', status_code=200)
#     self.assertEqual(response.context['user'], self.user)
    # self.assertIn('Пользователь', response.content.decode())
#
#
# def tearDown(self):
#     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', \
#                  'basketapp')
