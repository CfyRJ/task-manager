from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, RelatedFieldListFilter, ChoicesFieldListFilter

from .models import Tasks


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'author', 'executor', 'timestamp')
    search_fields = ['name']
    list_filter = (('timestamp', DateFieldListFilter),
                   ('status', RelatedFieldListFilter),
                   ('author', RelatedFieldListFilter),
                   ('executor', RelatedFieldListFilter),
                   ('labels', RelatedFieldListFilter),
                   )
