from typing import Any
from django.http import HttpRequest, HttpResponse
from django.forms.forms import BaseForm
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from django_filters.views import FilterView

from .models import Tasks
from .forms import TaskForm
from .filters import TasksFilter


class MixinMessage(LoginRequiredMixin):
    redirect_field_name = ""

    def get_login_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             'You are not authorized! Please come in.')
        return super().get_login_url()


class IndexSTasks(MixinMessage, FilterView):
    model = Tasks
    template_name = 'tasks/index_tasks.html'
    filterset_class = TasksFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)

        return context


class CreateTask(MixinMessage, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    extra_context = {'title': 'Create task'}
    success_url = reverse_lazy('index_tasks')
    success_message = 'Task successfully created'

    def form_valid(self, form: BaseForm):
        labels_id = form.cleaned_data['labels']
        task_name = form.cleaned_data['name']

        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()

        task = Tasks.objects.get(name=task_name)
        for label_id in labels_id:
            task.labels.add(label_id)

        messages.add_message(self.request,
                             messages.SUCCESS, self.success_message)

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
        labels = task.labels.all()
        return render(request,
                      'tasks/show_task.html',
                      context={
                          'task': task,
                          'labels': labels,
                      })
