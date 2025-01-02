from config import EmailSettings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


class EmailClient:
    def __init__(self, settings: EmailSettings):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_FROM,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
        self.fast_mail = FastMail(self.conf)

    async def send_email(self, subject: str, recipients: list[str], body: str):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype="html"
        )
        await self.fast_mail.send_message(message)
