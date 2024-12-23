from asyncio import gather, create_task
from .queue_consumer import QueueConsumer
from services.message_service import MessageProcessor
import logging
import asyncio
class ConsumerManager:
    def __init__(self, rabbitmq_url: str, queues: list[str]):
        self.rabbitmq_url = rabbitmq_url
        self.queues = queues
        self.consumers = []

    def setup_consumers(self):
        for queue in self.queues:
            processor = MessageProcessor()
            consumer = QueueConsumer(queue, self.rabbitmq_url, processor)
            self.consumers.append(consumer)

    async def start_all(self):
        loop = asyncio.get_event_loop()
        tasks = [create_task(consumer.start()) for consumer in self.consumers]
        await gather(*tasks)
