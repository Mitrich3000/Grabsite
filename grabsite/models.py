from django.db import models
from datetime import datetime

class Advertisement(models.Model):
    posted = models.DateTimeField(db_index=True, default = datetime.now)
