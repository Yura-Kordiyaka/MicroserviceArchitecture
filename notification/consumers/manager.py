from asyncio import gather, create_task
from .queue_consumer import QueueConsumer
from services.message_service import MessageProcessor
import logging
import asyncio
from handle_queues.handle_send_mail import NotificationEmail
from handle_queues.reset_password_queue import ResetPasswordQueue
from config import settings
class ConsumerManager:
    def __init__(self, rabbitmq_url: str, queues: list[str]):
        self.rabbitmq_url = rabbitmq_url
        self.queues = queues
        self.consumers = []
        self.processor = MessageProcessor()

    def setup_consumers(self):
        self.processor.register_handler(settings.queue_settings.user_creation_queue, NotificationEmail())
        self.processor.register_handler(settings.queue_settings.reset_password_queue, ResetPasswordQueue())

        for queue in self.queues:
            consumer = QueueConsumer(queue, self.rabbitmq_url, self.processor)
            self.consumers.append(consumer)

    async def start_all(self):
        loop = asyncio.get_event_loop()
        tasks = [create_task(consumer.start()) for consumer in self.consumers]
        await gather(*tasks)
