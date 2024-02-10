from django.db import models
from django.contrib.auth import get_user_model
from ..statuses.models import Status
from ..labels.models import Labels


class Tasks(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Name')
    description = models.TextField(blank=True, verbose_name='Description')
    status = models.ForeignKey(Status,
                               on_delete=models.PROTECT,
                               verbose_name='Status')
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.PROTECT,
                               related_name='tasks_author',
                               verbose_name='Author')
    executor = models.ForeignKey(get_user_model(),
                                 on_delete=models.PROTECT,
                                 blank=True, null=True,
                                 related_name='tasks_executor',
                                 verbose_name='Executor')
    labels = models.ManyToManyField(Labels, blank=True,
                                    related_name='labels',
                                    verbose_name='Labels')
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name='Date of creation')

    def __str__(self) -> str:
        return self.name
