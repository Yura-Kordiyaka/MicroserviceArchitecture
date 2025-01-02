from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class RabbitMQSettings(BaseSettings):
    host: str = os.environ.get('RABBITMQ_HOST')
    port: int = os.environ.get('RABBITMQ_PORT')
    user: str = os.environ.get('RABBITMQ_USER')
    password: str = os.environ.get('RABBITMQ_PASSWORD')


class EmailSettings(BaseSettings):
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD')
    MAIL_FROM: str = os.environ.get('MAIL_FROM')
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_DEBUG: bool = True


class QueueSettings(BaseSettings):
    user_creation_queue: str = os.environ.get('USER_CREATION_QUEUE')
    reset_password_queue: str = os.environ.get('USER_RESET_PASSWORD')

class Settings(BaseSettings):
    email_settings: EmailSettings = EmailSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    queue_settings: QueueSettings = QueueSettings()


settings = Settings()
