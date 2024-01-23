from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Statuse


class StatusesTests(TestCase):

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user_status',
                                            password='pass_status')

        cls.statuse1 = Statuse.objects.create(name='first status')
        cls.statuse2 = Statuse.objects.create(name='second status')
    
    def test_error_access(self):
        response_redirect = self.client.get('/statuses/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.get('/statuses/create/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.get('/statuses/1/update/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.get('/statuses/1/delete/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.post('/statuses/create/',
                                             {'name': 'test status'})
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.post('/statuses/1/update/',
                                             {'name': 'test status'})
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.post('/statuses/1/delete/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

    def test_successfull_access(self):
        self.client.login(username="user_status", password="pass_status")

        response = self.client.get('/statuses/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response = self.client.get('/statuses/create/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response = self.client.get('/statuses/1/update/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response = self.client.get('/statuses/1/delete/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_work_statuses(self):
        self.client.login(username="user_status", password="pass_status")

        response_redirect = self.client.post('/statuses/create/',
                                             {'name': 'test status'})
        response = self.client.get('/statuses/')
        content = response.content.decode()
        self.assertIn('Status successfully created', content)
        self.assertIn('test status', content)
        self.assertRedirects(response_redirect, '/statuses/', 302, 200)

        response_redirect = self.client.post('/statuses/3/update/',
                                             {'name': 'test status rename'})
        response = self.client.get('/statuses/')
        content = response.content.decode()
        self.assertIn('Status successfully changed', content)
        self.assertIn('test status rename', content)
        self.assertRedirects(response_redirect, '/statuses/', 302, 200)

        response_redirect = self.client.post('/statuses/3/delete/')
        response = self.client.get('/statuses/')
        content = response.content.decode()
        self.assertIn('Status deleted successfully', content)
        self.assertNotIn('test status rename', content)
        self.assertRedirects(response_redirect, '/statuses/', 302, 200)




