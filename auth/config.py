from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class DB_Settings(BaseSettings):
    DB_HOST: str = os.environ.get('DB_HOST')
    DB_PORT: int = os.environ.get('DB_PORT')
    DB_USER: str = os.environ.get('DB_USER')
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD')
    DB_NAME: str = os.environ.get('DB_NAME')


class TokenSettings(BaseSettings):
    ALGORITHM: str = os.environ.get('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES')
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY: str = os.environ.get('JWT_REFRESH_SECRET_KEY')


class RabbitMQSettings(BaseSettings):
    host: str = os.environ.get('RABBITMQ_HOST')
    port: int = os.environ.get('RABBITMQ_PORT')


class QueueSettings(BaseSettings):
    user_creation_queue: str = os.environ.get('USER_CREATION_QUEUE')
    reset_password_queue: str = os.environ.get('USER_RESET_PASSWORD')


class RedisSettings(BaseSettings):
    REDIS_PASSWORD: str = os.environ.get('REDIS_PASSWORD')
    REDIS_USER: str = os.environ.get('REDIS_USER')
    REDIS_USER_PASSWORD: str = os.environ.get('REDIS_USER_PASSWORD')


class GoogleSettings(BaseSettings):
    GOOGLE_CLIENT_ID: str = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_SECRET_ID: str = os.environ.get('GOOGLE_SECRET_ID')
    GOOGLE_REDIRECT_URL: str = os.environ.get('GOOGLE_REDIRECT_URL')


class Settings(BaseSettings):
    db: DB_Settings = DB_Settings()
    token: TokenSettings = TokenSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    queue_settings: QueueSettings = QueueSettings()
    redis_settings: RedisSettings = RedisSettings()
    google_settings: GoogleSettings = GoogleSettings()


settings = Settings()
