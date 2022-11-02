import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_SENT_FROM = os.environ.get('EMAIL_SENT_FROM')


ALLOWED_HOSTS.append(os.environ.get('POD_IP'))

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DNS'),
    integrations=[DjangoIntegration(), CeleryIntegration()],
    send_default_pii=True,
    traces_sample_rate=1.0
)
