from .base import *

DEBUG = True

# For email senging option
EMAIL_HOST = "smtp.mailtrap.io"
EMAIL_PORT = 2525
# os environ
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_SENT_FROM = os.environ.get("EMAIL_SENT_FROM")

# Используется для создания тестовой базы данных, если нет pg_dump
# В каждой модели есть классметод создания записей в бд
INIT_DB = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(";")
CORS_ALLOW_ALL_ORIGINS = True
