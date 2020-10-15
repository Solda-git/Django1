from django.core.management import call_command
from django.test import TestCase, Client


# Create your tests here.
class TestMainappSmoke(TestCase):
   def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()
