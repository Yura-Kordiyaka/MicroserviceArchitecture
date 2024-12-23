import aio_pika
import asyncio
import logging


class BaseConsumer:
    def __init__(self, queue_name: str, rabbitmq_url: str):
        self.queue_name = queue_name
        self.rabbitmq_url = rabbitmq_url

    async def connect(self):
        attempt = 0
        while attempt < 5:
            try:
                self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
                self.channel = await self.connection.channel()
                self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
                print(f"Connected to RabbitMQ, queue '{self.queue_name}' is ready.")
                return
            except aio_pika.exceptions.AMQPConnectionError as e:
                attempt += 1
                print(f"Attempt {attempt}: Failed to connect to RabbitMQ. Retrying in 5 seconds...")
                await asyncio.sleep(5)
        raise Exception("Failed to connect to RabbitMQ after 5 attempts")

    async def start(self):
        logging.info('Starting consumer')
        await self.connect()
        await self.consume()

    async def consume(self):
        async for message in self.queue:
            await self.on_message(message)

    async def on_message(self, message: aio_pika.IncomingMessage):
        raise NotImplementedError("Метод on_message має бути реалізований в підкласі.")