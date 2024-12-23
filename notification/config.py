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
    MAIL_PASSWORD: str = "your_email_password"
    MAIL_FROM: str = os.environ.get('MAIL_FROM')
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = True


class Settings(BaseSettings):
    email_settings: EmailSettings = EmailSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()


settings = Settings()
