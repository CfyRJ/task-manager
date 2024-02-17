from typing import Any
from django.http import HttpRequest, HttpResponse
from django.forms.forms import BaseForm
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from django_filters.views import FilterView

from .models import Tasks
from .forms import TaskForm
from .filters import TasksFilter


class MixinMessage(LoginRequiredMixin):
    redirect_field_name = ""

    def get_login_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             _('You are not authorized! Please come in.'))
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
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form: BaseForm):
        form.instance.author = self.request.user

        return super().form_valid(form)


class UpdateTask(MixinMessage, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('Task successfully changed')


class DeleteTask(MixinMessage, SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('Task deleted successfully')

    def get(self, request: HttpRequest,
            *args: str, **kwargs: Any) -> HttpResponse:
        user = request.user
        id_task = kwargs.get('pk')
        author = Tasks.objects.get(id=id_task).author
        if user != author:
            messages.add_message(self.request, messages.ERROR,
                                 _('Only its author can delete a task'))
            return redirect(reverse_lazy('index_tasks'))

        return super().get(request, *args, **kwargs)


class ShowTask(DetailView):
    model = Tasks
    template_name = 'tasks/show_task.html'
    context_object_name = 'task'
