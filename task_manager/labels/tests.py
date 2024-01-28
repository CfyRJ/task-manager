from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Labels
from ..statuses.models import Statuse
from ..tasks.models import Tasks


class LabelsTests(TestCase):

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user_auth = user_model.objects.create_user(username='user_auth_label',
                                                  password='pass_label',
                                                  first_name='user',
                                                  last_name='author')
        cls.user_exec = user_model.objects.create_user(username='user_exec_label',
                                                  password='pass_label',
                                                  first_name='user',
                                                  last_name='executor')

        cls.status = Statuse.objects.create(name='Status')

        cls.label_one = Labels.objects.create(name='One label')
        cls.label1_many = Labels.objects.create(name='Many1 label')
        cls.label2_many = Labels.objects.create(name='Many2 label')

        cls.task_one_l = Tasks.objects.create(name='task one label',
                                              status=cls.status,
                                              description='there is one label here',
                                              executor=cls.user_exec,
                                              author = cls.user_auth,
                                              labels = (cls.label_one, ))
        cls.task_many_l = Tasks.objects.create(name='task one label',
                                         status=cls.status,
                                         description='there are many labels here',
                                         executor=cls.user_exec,
                                         author = cls.user_auth,
                                         labels = (cls.label1_many,
                                                   cls.label2_many))

    def test_error_access(self):
        response_redirect = self.client.get('/labels/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.get('/labels/create/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.get('/labels/1/update/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.get('/labels/1/delete/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.post('/labels/create/',
                                             {'name': 'error labels'})
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.post('/labels/1/update/',
                                             {'name': 'error labels'})
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

        response_redirect = self.client.post('/labels/1/delete/')
        response = self.client.get('/login/')
        content = response.content.decode()
        self.assertIn('You are not authorized! Please come in.', content)
        self.assertRedirects(response_redirect, '/login/', 302, 200)

    def test_successfull_access(self):
        self.client.login(username="user_auth_label", password="pass_label")

        response = self.client.get('/labels/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response = self.client.get('/labels/create/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response = self.client.get('/labels/1/update/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response = self.client.get('/labels/1/delete/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_show_labels(self):
        self.client.login(username="user_auth_label", password="pass_label")

        response = self.client.get('/labels/')
        content = response.content.decode()
        self.assertIn('One label', content)
        self.assertIn('Many1 label', content)
        self.assertIn('Many2 label', content)

    def test_work_labels(self):
        self.client.login(username="user_auth_label", password="pass_label")

        response_redirect = self.client.post('/labels/create/',
                                             {'name': 'create new label'})
        response = self.client.get('/labels/')
        content = response.content.decode()
        self.assertIn('Label successfully created', content)
        self.assertIn('create new label', content)
        self.assertRedirects(response_redirect, '/labels/', 302, 200)

        response = self.client.post('/labels/create/',
                                             {'name': 'create new label'})
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        content = response.content.decode()
        self.assertIn('A label with the same name already exists.', content)

        new_label = Labels.objects.get(id=4)

        self.task_many_l = Tasks.objects.update(name='task one label',
                                         status=self.status,
                                         description='there are many labels here',
                                         executor=self.user_exec,
                                         author = self.user_auth,
                                         labels = (self.label1_many,
                                                   self.label2_many,
                                                   new_label))
        labels_task_many_1 = self.task_many_l.objects.labels
        self.assertIn(new_label, labels_task_many_1)

        response_redirect = self.client.post('/labels/4/update',
                                             {'name': 'change new label'})
        response = self.client.get('/labels/')
        content = response.content.decode()
        self.assertIn('Label successfully changed', content)
        self.assertIn('change new label', content)
        self.assertRedirects(response_redirect, '/labels/', 302, 200)

        new_label = Labels.objects.get(id=4)
        labels_task_many_1 = self.task_many_l.objects.labels
        self.assertIn(new_label, labels_task_many_1)

        response = self.client.post('/labels/4/delete/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        content = response.content.decode()
        self.assertIn('The label cannot be deleted because it is in use.', content)

        self.task_many_l = Tasks.objects.update(name='task one label',
                                         status=self.status,
                                         description='there are many labels here',
                                         executor=self.user_exec,
                                         author = self.user_auth,
                                         labels = (self.label1_many,
                                                   self.label2_many,))
        new_label = Labels.objects.get(id=4)
        labels_task_many_1 = self.task_many_l.objects.labels
        self.assertNotIn(new_label, labels_task_many_1)

        response_redirect = self.client.post('/labels/4/delete/')
        response = self.client.get('/labels/')
        content = response.content.decode()
        self.assertIn('Label deleted successfully', content)
        self.assertNotIn('change new label', content)
        self.assertRedirects(response_redirect, '/labels/', 302, 200)
