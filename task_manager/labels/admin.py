from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import Labels


@admin.register(Labels)
class LabelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'timestamp')
    search_fields = ['name']
    list_filter = (('timestamp', DateFieldListFilter),)
