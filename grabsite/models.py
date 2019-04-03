from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateTimeField(db_index=True, default=datetime.now)


class Urls(models.Model):
    user = models.ManyToManyField(User, blank=True)
    name = models.CharField('Название', max_length=100)
    grabed = models.DateTimeField(db_index=True, default=datetime.now)