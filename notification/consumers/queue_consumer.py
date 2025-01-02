import json
import logging
import aio_pika
from .base import BaseConsumer
from services.message_service import MessageProcessor
from config import settings


class QueueConsumer(BaseConsumer):
    def __init__(self, queue_name: str, rabbitmq_url: str, processor: MessageProcessor):
        super().__init__(queue_name, rabbitmq_url)
        self.processor = processor

    async def on_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                body = json.loads(message.body.decode())

                await self.processor.process_message(queue_name=self.queue_name, data=body)

            except Exception as e:
                logging.error(f"Помилка обробки повідомлення: {e}")
