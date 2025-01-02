from .base import BaseQueueHandle
from services.email_client import EmailClient
from config import settings
import logging

class ResetPasswordQueue(BaseQueueHandle):
    def __init__(self):
        self.email_client = EmailClient(settings.email_settings)
    async def handle(self, data: dict):
        subject=data.get('subject','default subject')
        recipients =[data.get('email')]
        body = data.get('body', 'Default Email Body')

        try:
            await self.email_client.send_email(subject, recipients, body)
            logging.info(f"Email sent successfully to: {recipients}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
