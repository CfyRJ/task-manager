from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _
from django.contrib import messages

from django.contrib.auth.views import LoginView
from .forms import LoginUserForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LogoutView

from django.http import HttpResponse


class IndexView(View):
    def get(self, request, *args, **kwargs):

        # messages.add_message(request, messages.INFO, "Hi me!")
        # messages.add_message(request, messages.ERROR, "Hi me!")
        # messages.add_message(request, messages.SUCCESS, "Hi me!")
        messages_ = messages.get_messages(request)

        return render(
            request,
            'index.html',
            context={
                'messages': messages_
            }
        )


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    extra_context = {'title': 'Register'}
    success_message = 'You are logged in'


class LogoutUser(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are logged out.")
        return super().dispatch(request, *args, **kwargs)
