from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_account_email_template(
    email_to: EmailStr,
):
    email = EmailMessage()
    email["From"] = settings.SMTP_USER
    email["Subject"] = "Создание аккаунта"
    email["To"] = email_to

    email.set_content(
        """
            <h1>Здравствуйте!</h1>
            <h2>Вы создали аккаунт на сайте WHYCHAT.
            Этот сайт является моим pet-проектом. Я непрерывно работаю над
            внедрением нового функционала и улучшенных практик создания REST API.
            </h2>
            <h3>Спасибо за регистрацию! <br>
            С уважением, Дмитрий Кантемиров</h3>
        """,
        subtype="html",
    )

    return email
