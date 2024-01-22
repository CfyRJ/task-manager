from django.db import models

# Create your models here.
class Statuse(models.Model):
    name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
