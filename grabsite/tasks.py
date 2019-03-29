from celery.task import task
from grab import Grab
import requests
import bs4
from django.core.mail import send_mail
import re
from datetime import datetime
import logging
from .models import Advertisement


@task
def mail_sent(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    url = 'https:\\mysite.com\\result'
    subject = 'Анализ запрошенного ресурса'
    message = 'Графики по анализу запрошенного ресурса {}.'.format(url)
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          ['user@mail.ru,'])
    return mail_sent


def data_mining(links):
    date_list = []
    for link in links:
        data = requests.get(link)
        dom = bs4.BeautifulSoup(data.text, features="lxml")
        text = dom.find('em').text
        time = re.search(r'(\d{2}:\d{2})', text)
        s = text.split(',')
        s = s[1].strip()
        date_str = s.replace('марта', '3') + ' ' + time.group()
        date = datetime.strptime(date_str, '%d %m %Y %H:%S')
        advertisement = Advertisement(posted=date.astimezone())
        date_list.append(advertisement)

    return date_list


@task
def parsing():
    # parsing url
    links = []
    url = 'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/arenda-kvartir-komnat/'

    try:
        data = requests.get(url)
        dom = bs4.BeautifulSoup(data.text, features="lxml")
        links = dom.select('.marginright5')
        links = [item.get('href') for item in links]
    except:
        print('Error grabbing')
    # grab links
    data_mining(links)
    # add dates in model
    advertisements = Advertisement.objects.all()
    if advertisements.exists():
        Advertisement.objects.all()._raw_delete(advertisements.db)
    Advertisement.objects.bulk_create(data_mining(links))
    print('Данные добавлены')
    # show graph
    return url
