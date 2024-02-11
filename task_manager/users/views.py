from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.db.models.deletion import ProtectedError

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .forms import CreateUserForm


MESS_PERMISSION = _("You do not have permission to modify another user.")


class IndexIndex(View):

    def get(self, request, *args, **kwargs):
        users = get_user_model().objects.order_by('id')

        messages_ = messages.get_messages(request)
        return render(request,
                      'users/index.html',
                      context={
                          'messages': messages_,
                          'users': users,
                      })


class CreateUser(SuccessMessageMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'users/create_user.html'
    extra_context = {'title': _('Authorization user')}
    success_url = reverse_lazy('login')
    success_message = _('You have successfully registered')


class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = CreateUserForm
    template_name = 'users/update_user.html'
    extra_context = {'title': _('Change user')}
    success_url = reverse_lazy('index_users')
    success_message = _('User successfully changed')

    def get(self, request: HttpRequest,
            *args: str, **kwargs: Any) -> HttpResponse:
        user_id = self.get_object().id
        url_id = kwargs.get('id')
        if url_id != user_id:
            messages.add_message(self.request, messages.ERROR,
                                 MESS_PERMISSION)
            return redirect(reverse_lazy('index_users'))

        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        user = self.request.user
        return user

    def form_valid(self, form):
        password = form.cleaned_data.get('password1')
        if password:
            self.object.set_password(password)
        return super().form_valid(form)


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'users/delete_user.html'
    extra_context = {'title': _('Deleting a user')}
    success_url = reverse_lazy('index_users')
    success_message = _('User deleted successfully')

    def get(self, request: HttpRequest,
            *args: str, **kwargs: Any) -> HttpResponse:
        user_id = self.get_object().id
        url_id = kwargs.get('id')
        if url_id != user_id:
            messages.add_message(self.request, messages.ERROR,
                                 MESS_PERMISSION)
            return redirect(reverse_lazy('index_users'))

        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        user = self.request.user
        return user

    def post(self,
             request: HttpRequest,
             *args: str,
             **kwargs: Any) -> HttpResponse:
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR,
                _("The user cannot be deleted because it is in use.")
                )
            return redirect(reverse_lazy('index_users'))
