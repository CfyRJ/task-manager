from django.forms import ModelForm
from .models import Statuse


class StatuseForm(ModelForm):
    class Meta:
        model = Statuse
        fields = ('name', )
