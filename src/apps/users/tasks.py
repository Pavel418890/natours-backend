from smtplib import SMTPConnectError, SMTPException
from typing import List

from celery import Task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

from apps.config.celery import app


@app.task(name="apps.users.health-check", max_retries=3)
def check(a: int, b: int) -> Task:
    return a + b


@app.task(
    name="apps.users.services.send_email_address_confirmation",
    auto_retry=[SMTPConnectError, SMTPException],
    max_retries=3,
)
def send_email_address_confirmation(
    recipient_list: List[str], confirmation_token: str
) -> Task:
    """
    Отправляет письмо подтверждения статуса пользователя на email адрес
    """
    context = {
        "email_confirmation_url": f"{settings.CLIENT_BASE_URL}/email-confirmation/{confirmation_token}/"
    }

    email_confirmation_template = render_to_string("email-confirmation.html", context)
    with get_connection() as connection:
        email = EmailMultiAlternatives(
            subject="Welcome",
            from_email=settings.EMAIL_SENT_FROM,
            to=recipient_list,
            connection=connection,
        )
        email.attach_alternative(email_confirmation_template, "text/html")
        email.send()


@app.task(
    name="apps.users.services.send_reset_password",
    auto_retry=[SMTPConnectError],
    max_retries=3,
)
def send_reset_password(recipient_list: List[str], reset_token: str) -> Task:
    """Отправляет письмо пользователю на восстановление пароля"""

    context = {
        "password_reset_token": f"{settings.CLIENT_BASE_URL}/reset-password/{reset_token}/"
    }
    password_reset_token_template = render_to_string("reset_password.html", context)
    with get_connection() as connection:
        email = EmailMultiAlternatives(
            subject="Natours Reset Password",
            from_email=settings.EMAIL_SENT_FROM,
            to=recipient_list,
            connection=connection,
        )
        email.attach_alternative(password_reset_token_template, "text/html")
        email.send()
