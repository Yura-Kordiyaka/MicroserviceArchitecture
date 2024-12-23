from fastapi import FastAPI, APIRouter
from consumers.manager import ConsumerManager
from config import settings
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    rabbitmq_url = f"amqp://{settings.rabbitmq.password}:{settings.rabbitmq.user}@{settings.rabbitmq.host}:{settings.rabbitmq.port}/"
    queues = ["notification_create_user"]
    consumer_manager = ConsumerManager(rabbitmq_url, queues)
    consumer_manager.setup_consumers()
    await consumer_manager.start_all()