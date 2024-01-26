from typing import Any
from django.forms.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.http import request

from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .models import Tasks

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import TaskForm

from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from django.shortcuts import redirect


class MixinMessage(LoginRequiredMixin):
    redirect_field_name = ""

    def get_login_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             'You are not authorized! Please come in.')
        return super().get_login_url()


class IndexSTasks(MixinMessage,  View):
    def get(self, request, *args, **kwargs):
        tasks = Tasks.objects.order_by('id')

        messages_ = messages.get_messages(request)
        return render(request,
                      'tasks/index_tasks.html',
                      context={
                          'messages': messages_,
                          'tasks': tasks,
                      })


class CreateTask(MixinMessage, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    extra_context = {'title': 'Create task'}
    success_url = reverse_lazy('index_tasks')
    success_message = 'Task successfully created'

    def form_valid(self, form: BaseForm):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()

        messages.add_message(self.request, messages.SUCCESS, self.success_message)

        return redirect(self.success_url)


class UpdateTask(MixinMessage, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    extra_context = {'title': 'Change of task'}
    success_url = reverse_lazy('index_tasks')
    success_message = 'Task successfully changed'


class DeleteTask(MixinMessage, SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete_task.html'
    extra_context = {'title': 'Deleting a task'}
    success_url = reverse_lazy('index_tasks')
    success_message = 'Task deleted successfully'

    def get(self, request: HttpRequest,
            *args: str, **kwargs: Any) -> HttpResponse:
        user = request.user
        id_task = kwargs.get('pk')
        author = Tasks.objects.get(id=id_task).author
        if user != author:
            messages.add_message(self.request, messages.ERROR,
                                 'Only its author can delete a task')
            return redirect(reverse_lazy('index_tasks'))

        return super().get(request, *args, **kwargs)


class ShowTask(View):
    def get(self, request, *args, **kwargs):
        id_task = kwargs.get('pk')
        task = Tasks.objects.get(id=id_task)
        return render(request,
                      'tasks/show_task.html',
                      context={
                          'task': task,
                      })
