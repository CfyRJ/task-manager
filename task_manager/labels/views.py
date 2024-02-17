from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Labels
from .forms import LabelForm

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class NoAuthMixin(LoginRequiredMixin):
    redirect_field_name = ""

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('You are not authorized! Please come in.')
        self.permission_denied_url = reverse_lazy('login')
        return super().dispatch(request, *args, **kwargs)


class NoPermissionMixin:

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(self.permission_denied_url)


class IndexLabels(NoPermissionMixin, NoAuthMixin, ListView):
    model = Labels
    template_name = 'labels/index_labels.html'
    context_object_name = 'labels'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context


class CreateLabel(NoPermissionMixin, NoAuthMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/create_label.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('Label successfully created')


class UpdateLabel(NoPermissionMixin, NoAuthMixin, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('Label successfully changed')


class DeleteLabel(NoPermissionMixin, NoAuthMixin, SuccessMessageMixin, DeleteView):
    model = Labels
    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('Label deleted successfully')
    error_del_message = _("The label cannot be deleted because it is in use.")

    def post(self, request: HttpRequest,
             *args: str, **kwargs: Any) -> HttpResponse:
        label_id = kwargs.get('pk')
        label = Labels.objects.get(id=label_id)
        tasks = label.labels.all()

        if tasks:
            messages.add_message(request, messages.ERROR,
                                 self.error_del_message)
            return redirect(reverse_lazy('index_labels'))

        return super().post(request, *args, **kwargs)
