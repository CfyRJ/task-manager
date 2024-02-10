from django.db import models


# Create your models here.
class Labels(models.Model):
    name = models.CharField(max_length=200, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
