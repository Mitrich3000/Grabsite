# import celery
from .celery import app as celery_app

CELERY_ALWAYS_EAGER = True