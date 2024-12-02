import smtplib

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_template import create_account_email_template


@celery.task
def send_confirmation_email(email_to: EmailStr):
    msg_content = create_account_email_template(email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
