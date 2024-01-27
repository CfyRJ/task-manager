from django.test import TestCase, Client
from django.contrib.auth import get_user_model



class UserslTests(TestCase):

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(username='utest',
                                            password='ptest')
        cls.user = user_model.objects.create_user(username='utest1',
                                            password='ptest1')

    def test_users(self):
        response = self.client.get('/users/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        content = response.content.decode()
        self.assertIn('utest', content)

    def test_create_user(self):
        response = self.client.get('/users/create/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response_redirect = self.client.post('/users/create/',
                                             {"username": "utest2",
                                              "password1": "ptest2",
                                              "password2": "ptest2"})

        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You have successfully registered', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

    def test_error_create_user(self):
        response = self.client.post('/users/create/', {"username": "utest#",
                                                       "password1": "ptest2",
                                                       "password2": "ptest2"})
        content = response.content.decode()
        self.assertIn('numbers and the symbols @/./+/-/_.', content)

        response = self.client.post('/users/create/', {"username": "utest3",
                                                       "password1": "p",
                                                       "password2": "p"})
        content = response.content.decode()
        self.assertIn('This password is too short.', content)

        response = self.client.post('/users/create/', {"username": "utest",
                                                       "password1": "ppp",
                                                       "password2": "ppp"})
        content = response.content.decode()
        self.assertIn('A user with that username already exists.', content)

    def test_update_user(self):
        self.client.login(username="utest1", password="ptest1")
        response_redirect = self.client.get('/users/1/update/')

        response = self.client.get('/users/')
        content = response.content.decode()
        self.assertIn('You do not have permission to modify another user.',
                      content)
        self.assertRedirects(response_redirect, '/users/', 302, 200)

        response = self.client.get('/users/7/update/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response_redirect = self.client.post('/users/4/update/',
                                             {"username": "utest10",
                                              "password1": "ptest10",
                                              "password2": "ptest10"})

        response = self.client.get('/users/')
        content = response.content.decode()
        self.assertIn('User successfully changed', content)
        self.assertIn('utest10', content)
        self.assertIn('Log In', content)
        self.assertRedirects(response_redirect, '/users/', 302, 200)

        self.client.login(username="utest10", password="ptest10")
        response = self.client.get('/users/7/update/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_delete_user(self):
        self.client.login(username="utest1", password="ptest1")
        response_redirect = self.client.get('/users/1/delete/')

        response = self.client.get('/users/')
        content = response.content.decode()
        self.assertIn('You do not have permission to modify another user.',
                      content)
        self.assertRedirects(response_redirect, '/users/', 302, 200)

        response = self.client.get('/users/7/delete/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        content = response.content.decode()
        self.assertIn('utest1', content)

        response_redirect = self.client.post('/users/7/delete/')

        response = self.client.get('/users/')
        content = response.content.decode()
        self.assertIn('User deleted successfully', content)
        self.assertNotIn('utest1', content)
        self.assertIn('Log In', content)
        self.assertRedirects(response_redirect, '/users/', 302, 200)
