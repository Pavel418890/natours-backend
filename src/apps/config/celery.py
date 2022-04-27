
from . import celeryconfig
from celery import Celery, signals


app = Celery('apps')
app.config_from_object(celeryconfig)

app.autodiscover_tasks()
