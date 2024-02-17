from typing import Any
from django.http import HttpRequest, HttpResponse
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Status
from .forms import StatusForm


class MixinMessage(LoginRequiredMixin):
    redirect_field_name = ""

    def get_login_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             _('You are not authorized! Please come in.'))
        return super().get_login_url()


class IndexStatuses(MixinMessage, View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.order_by('id')

        messages_ = messages.get_messages(request)
        return render(request,
                      'statuses/index_statuses.html',
                      context={
                          'messages': messages_,
                          'statuses': statuses,
                      })


class CreateStatus(MixinMessage, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    template_name = 'statuses/create_status.html'
    success_url = reverse_lazy('index_statuses')
    success_message = _('Status successfully created')


class UpdateStatus(MixinMessage, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update_status.html'
    success_url = reverse_lazy('index_statuses')
    success_message = _('Status successfully changed')


class DeleteStatus(MixinMessage, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('index_statuses')
    success_message = _('Status deleted successfully')
    error_del_message = _("The status cannot be deleted because it is in use.")

    def post(self,
             request: HttpRequest,
             *args: str,
             **kwargs: Any) -> HttpResponse:
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(request, messages.ERROR,
                                 self.error_del_message)
            return redirect(reverse_lazy('index_statuses'))
