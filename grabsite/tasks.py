import re
from datetime import datetime
from itertools import groupby, count

import bs4
import requests
from celery.task import task
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay, ExtractHour

from test2 import settings
from .models import Advertisement, Urls


@task
def mail_sent():
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """

    url = settings.SITE_URL + '\charts'
    subject = 'Анализ запрошенного ресурса'
    message = 'Графики популярного часа дня и дня недели {}'.format(url)
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          ['user@mail.ru,'])
    print(message)
    return mail_sent


def data_mining(links):
    """
    Grabbing urls
    """

    date_list = []
    for link in links:
        data = requests.get(link)
        dom = bs4.BeautifulSoup(data.text, features="lxml")
        try:
            text = dom.find('em').text
            time = re.search(r'(\d{2}:\d{2})', text)
            s = text.split(',')
            s = s[1].strip()
            months = {'января': '1', 'февраля': '2', 'марта': '3', 'апреля': '4', 'мая': '5', 'июня': '6', 'июля': '7',
                      'августа': '8', 'сентября': '9', 'октября': '10', 'ноября': '11', 'декабря': '12'}
            for k, v in months.items():
                if k in s:
                    s = s.replace(k, v)
            date_str = f'{s} {time.group()}'
            date = datetime.strptime(date_str, '%d %m %Y %H:%M')
            date_list.append(date)
        except:
            print("Ошибка обработки запроса")

    return date_list


def get_weekday(dates):
    """Return weekday."""

    field = lambda x: x.isoweekday()
    weekday = dict([(weekday, sum(1 for _ in items)) for weekday, items in groupby(dates, field)])
    data = {i: 0 for i in range(1,8)}
    data.update(weekday)
    data = [[v for k, v in data.items()]]

    return data


def get_poptime(dates):
    """Return poptime."""

    field = lambda x: x.hour
    poptime = dict([(poptime, sum(1 for _ in items)) for poptime, items in groupby(dates, field)])
    data = {i: 0 for i in range(24)}
    data.update(poptime)
    data = [[v for k, v in data.items()]]

    return data


@task
def parsing(user, url):
    # parsing url
    links = []
    try:
        data = requests.get(url)
        dom = bs4.BeautifulSoup(data.text, features="lxml")
        links = dom.select('.marginright5')
        links = [item.get('href') for item in links]
    except:
        print('Error grabbing')
    # grab links
    data = data_mining(links)
    # add dates in model
    urls = Urls(user=user, name=url, weekday=get_weekday(data), poptime=get_poptime(data))
    urls.save()
    print('Данные добавлены')
    # mail_sent()
    return
