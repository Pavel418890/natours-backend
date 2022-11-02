import os

from django.conf import settings

broker_url = settings.RABBIT_DSN
result_backend = settings.REDIS_DSN
