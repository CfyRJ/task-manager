from django_filters import FilterSet
from .models import Tasks
from django import forms
from django_filters import ChoiceFilter, BooleanFilter
from ..labels.models import Labels


class TasksFilter(FilterSet):
    labels = ChoiceFilter(choices=lambda: [(label.id, label.name) for label in Labels.objects.all()])
    author = BooleanFilter(widget=forms.CheckboxInput, method='filter_author')

    def filter_author(self, queryset, *args, **kwargs):
        author = args[-1]
        if author:
            author = getattr(self.request, 'user', None)
            return queryset.filter(author=author)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels', 'author']
