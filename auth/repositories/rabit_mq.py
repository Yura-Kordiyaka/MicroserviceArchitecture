import aio_pika
from config import settings
import json


class RabbitMQRepository:
    _connection = None
    _channel = None

    @classmethod
    async def get_connection(cls):
        if cls._connection is None or cls._connection.is_closed:
            cls._connection = await aio_pika.connect_robust(
                f"amqp://admin:admin@{settings.rabbitmq.host}:{settings.rabbitmq.port}/"
            )
        return cls._connection

    @classmethod
    async def get_channel(cls):
        if cls._channel is None or cls._channel.is_closed:
            connection = await cls.get_connection()
            cls._channel = await connection.channel()
        return cls._channel

    @classmethod
    async def publish(cls, message: dict, routing_key: str):
        channel = await cls.get_channel()
        message_json = json.dumps(message).encode()
        await channel.declare_queue(routing_key, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_json),
            routing_key=routing_key,
        )
