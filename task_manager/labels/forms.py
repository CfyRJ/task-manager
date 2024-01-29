from django.forms import ModelForm
from .models import Labels


class LabelForm(ModelForm):
    class Meta:
        model = Labels
        fields = ('name', )
