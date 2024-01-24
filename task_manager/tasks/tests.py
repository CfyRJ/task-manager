from django.test import TestCase, Client
from django.contrib.auth.models import User
from ..statuses.models import Statuse
from .models import Tasks


class TasksTests(TestCase):

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='user1_tasks',
                                            password='pass1_tasks',
                                            first_name='fname1',
                                            last_name='lname1')
        cls.user2 = User.objects.create_user(username='user2_tasks',
                                            password='pass2_tasks',
                                            first_name='fname2',
                                            last_name='lname2')
        cls.user3 = User.objects.create_user(username='user3_tasks',
                                            password='pass3_tasks',
                                            first_name='fname3',
                                            last_name='lname3')

        cls.statuse1 = Statuse.objects.create(name='first status')
        cls.statuse2 = Statuse.objects.create(name='second status')
        cls.statuse3 = Statuse.objects.create(name='third status')

        cls.task1 = Tasks.objects.create(name='task1',
                                         status=cls.statuse1,
                                         description='Fuh1',
                                         executor=cls.user2,
                                         author = cls.user1)

    def test_error_access(self):
        response_redirect = self.client.get('/tasks/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.get('/tasks/create/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.get('/tasks/1/update/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.get('/tasks/1/delete/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.post('/tasks/create/',
                                             {'name': 'task1',
                                              'status': self.statuse1,
                                              'description': 'Fuh1',
                                              'executor': self.user2,
                                              'author': self.user1})
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.post('/tasks/1/update/',
                                             {'name': 'task1',
                                              'status': self.statuse1,
                                              'description': 'Fuh1',
                                              'executor': self.user2,
                                              'author': self.user1})
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.post('/tasks/1/delete/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

    def test_successfull_access(self):
        self.client.login(username="user1_tasks", password="pass1_tasks")

        response = self.client.get('/tasks/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response = self.client.get('/tasks/create/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response = self.client.get('/tasks/1/update/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response = self.client.get('/tasks/1/delete/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_work_tasks(self):
        self.client.login(username="user3_tasks", password="user3_tasks")

        response = self.client.get('/tasks/')
        content = response.content.decode()
        self.assertIn('task1', content)
        self.assertIn('first status', content)
        self.assertIn('fname1 lname1', content)
        self.assertIn('fname2 lname2', content)

        response_redirect = self.client.post('/tasks/create/',
                                             {'name': 'task2',
                                              'status': self.statuse2,
                                              'description': 'Fuh2',
                                              'executor': self.user2})
        response = self.client.get('/tasks/')
        content = response.content.decode()
        self.assertIn('Tasks successfully created', content)
        self.assertIn('task2', content)
        self.assertIn('second status', content)
        self.assertIn('fname3 lname3', content)
        self.assertIn('fname2 lname2', content)
        self.assertRedirects(response_redirect, '/tasks/', 302, 200)

        response_redirect = self.client.post('/tasks/2/update/',
                                             {'name': 'task2 update',
                                              'status': self.statuse2,
                                              'description': 'Fuh2',
                                              'executor': self.user2})
        response = self.client.get('/tasks/')
        content = response.content.decode()
        self.assertIn('Tasks successfully changed', content)
        self.assertIn('task2 update', content)
        self.assertRedirects(response_redirect, '/tasks/', 302, 200)

        response_redirect = self.client.post('/tasks/2/delete/')
        response = self.client.get('/tasks/')
        content = response.content.decode()
        self.assertIn('Tasks deleted successfully', content)
        self.assertNotIn('task2 update', content)
        self.assertRedirects(response_redirect, '/tasks/', 302, 200)
