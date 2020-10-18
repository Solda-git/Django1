from django.core.management import call_command
from django.test import TestCase, Client


# Create your tests here.
from kwauth.models import KWUser


class TestUserManagement(TestCase):

    # fixtures = ['kwauth.json', 'main.json', 'cart.json', 'orders.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        #
        # def setUp(self):
        #     self.client = Client()
        cls.superuser = KWUser.objects.create_superuser('django2', 'django2@geekshop.local', 'geekbrains')
        cls.user = KWUser.objects.create_user('solda2', 'solda2@geekshop.local', 'geekbrains')
        cls.user_with__first_name = KWUser.objects.create_user('knitted', 'knitted@geekshop.local', 'geekbrains',
                                                               first_name='Knitted world')


    def test_user_login(self):
        # главная без логина
        print('test_user_login')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['page_title'], 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)
        # print(response.content.decode('utf-8'))
        self.assertNotIn('Пользователь', response.content.decode('utf-8'))
        # self.client.login(username='solda2', password='geekbrains')
        print('<><><><><><><><><><><><><>')
        self.client.post('/auth/login/',
                         data={
                              'username': 'solda2',
                              'password': 'geekbrains'
                         }
                        )
        # # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=200)
        self.assertEqual(response.context['user'], self.user)

    def test_cart_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/cart/')
        self.assertEqual(response.url, '/auth/login/?next=/cart/')
        self.assertEqual(response.status_code, 302)

        # с логином все должно быть хорошо
        self.client.login(username='knitted', password='geekbrains')

        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(list(response.context['cart']), [])
        self.assertEqual(response.request['PATH_INFO'], '/cart/')
        print(response.content.decode())
        self.assertIn('КОРЗИНА', response.content.decode('utf-8'))

    #
    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')