import json
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateTimeField(db_index=True, default=datetime.now)


class Urls(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=100)
    grabed = models.DateTimeField('Обработано', auto_now_add=True)
    weekday = models.TextField('Популярный день недели')
    poptime = models.TextField('Популярное время')

    def get_weekday_dict(self):
        dict = json.loads(self.weekday)

        return dict

    def get_poptime_dict(self):
        dict = json.loads(self.poptime)

        return dict

    def __str__(self):
        return 'Адрес {self.name}, от {self.grabed}'

    def get_absolute_url(self):
        return reverse('grabsite:detail', kwargs={'pk': self.pk})