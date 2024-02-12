from django.utils.translation import gettext_lazy as _

from django_filters import FilterSet
from django_filters import ChoiceFilter, BooleanFilter

from django import forms
from .models import Tasks
from ..labels.models import Labels


class TasksFilter(FilterSet):
    label = ChoiceFilter(
        choices=lambda: [(label.id, label.name)
                         for label
                         in Labels.objects.all()],
        field_name='labels',
        label=_('Label'),
    )
    self_tasks = BooleanFilter(widget=forms.CheckboxInput,
                               method='filter_author',
                               label=_('Only your tasks'))

    def filter_author(self, queryset, *args, **kwargs):
        author = args[-1]
        if author:
            author = getattr(self.request, 'user', None)
            return queryset.filter(author=author)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'label', 'self_tasks']
