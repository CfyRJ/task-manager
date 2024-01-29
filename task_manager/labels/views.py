from typing import Any
from django.forms.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .models import Labels

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import LabelForm

from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from django.shortcuts import redirect


class MixinMessage(LoginRequiredMixin):
    redirect_field_name = ""

    def get_login_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             'You are not authorized! Please come in.')
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
    extra_context = {'title': 'Create label'}
    success_url = reverse_lazy('index_labels')
    success_message = 'Label successfully created'


class UpdateLabel(MixinMessage, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = 'labels/update_label.html'
    extra_context = {'title': 'Change of label'}
    success_url = reverse_lazy('index_labels')
    success_message = 'Label successfully changed'


class DeleteLabel(MixinMessage, SuccessMessageMixin, DeleteView):
    model = Labels
    template_name = 'labels/delete_label.html'
    extra_context = {'title': 'Deleting a label'}
    success_url = reverse_lazy('index_labels')
    success_message = 'Label deleted successfully'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        label_id = kwargs.get('pk')
        label = Labels.objects.get(id=label_id)
        tasks = label.labels.all()

        if tasks:
            messages.add_message(request, messages.ERROR,
                                 "The label cannot be deleted because it is in use.")
            return redirect(reverse_lazy('index_labels'))

        return super().post(request, *args, **kwargs)
