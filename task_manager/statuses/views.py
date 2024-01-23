from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .models import Statuse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import StatuseForm

from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from django.shortcuts import redirect


class MixinMessage(LoginRequiredMixin):
    redirect_field_name = ""

    def get_login_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             'You are not authorized! Please come in.')
        return super().get_login_url()


class IndexStatuses(MixinMessage,  View):

    def get(self, request, *args, **kwargs):
        statuses = Statuse.objects.order_by('id')

        messages_ = messages.get_messages(request)
        return render(request,
                      'statuses/index_statuses.html',
                      context={
                          'messages': messages_,
                          'statuses': statuses,
                      })


class CreateStatuse(MixinMessage, SuccessMessageMixin, CreateView):
    form_class = StatuseForm
    template_name = 'statuses/create_statuse.html'
    extra_context = {'title': 'Create status'}
    success_url = reverse_lazy('index_statuses')
    success_message = 'Status successfully created'


class UpdateStatuse(MixinMessage, SuccessMessageMixin, UpdateView):
    model = Statuse
    form_class = StatuseForm
    template_name = 'statuses/update_statuse.html'
    extra_context = {'title': 'Change of status'}
    success_url = reverse_lazy('index_statuses')
    success_message = 'Status successfully changed'


class DeleteStatuse(MixinMessage, SuccessMessageMixin, DeleteView):
    model = Statuse
    template_name = 'statuses/delete_statuse.html'
    extra_context = {'title': 'Deleting a status'}
    success_url = reverse_lazy('index_statuses')
    success_message = 'Status deleted successfully'
