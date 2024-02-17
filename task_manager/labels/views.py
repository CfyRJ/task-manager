from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Labels
from .forms import LabelForm

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class MixinMessage(LoginRequiredMixin):
    redirect_field_name = ""

    def get_login_url(self, *args, **kwargs):
        text_messages = _('You are not authorized! Please come in.')
        messages.add_message(self.request, messages.ERROR,
                             text_messages)
        return super().get_login_url()


class IndexLabels(MixinMessage, View):
    def get(self, request, *args, **kwargs):
        labels = Labels.objects.order_by('id')

        messages_ = messages.get_messages(request)
        return render(request,
                      'labels/index_labels.html',
                      context={
                          'messages': messages_,
                          'labels': labels,
                      })


class CreateLabel(MixinMessage, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/create_label.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('Label successfully created')


class UpdateLabel(MixinMessage, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('Label successfully changed')


class DeleteLabel(MixinMessage, SuccessMessageMixin, DeleteView):
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
