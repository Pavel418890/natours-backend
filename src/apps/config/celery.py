from celery import Celery, signals

from . import celeryconfig

app = Celery("apps")
app.config_from_object(celeryconfig)

app.autodiscover_tasks()
