import json
import logging
import aio_pika
from .base import BaseConsumer
from services.message_service import MessageProcessor
class QueueConsumer(BaseConsumer):
    def __init__(self, queue_name: str, rabbitmq_url: str, processor: MessageProcessor):
        super().__init__(queue_name, rabbitmq_url)
        self.processor = processor

    async def on_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                body = json.loads(message.body.decode())
                logging.info(f"recive message is: {body}")

                await self.processor.process_message('notification_create_user',body)

            except Exception as e:
                logging.error(f"Помилка обробки повідомлення: {e}")
