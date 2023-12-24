from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.translation import gettext as _


class IndexView(View):
    def get(self, request, *args, **kwargs):

        return render(
            request,
            'index.html',
        )
