from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Statuse


class InitialTests(TestCase):

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='utest',
                                            password='ptest')

        cls.user = Statuse.objects.create(name='first status')
        cls.user = Statuse.objects.create(name='second status')
    
    def test_access(self):
        pass



