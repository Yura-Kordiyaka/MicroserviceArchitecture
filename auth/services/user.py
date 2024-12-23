from abc import ABC, abstractmethod
from fastapi import HTTPException
from repositories.user import UserRepository
from repositories.token import JWTTokenRepository
from schemas.user import UserCreate, ResponseUserForm
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import Token
from utils.password import get_hashed_password, verify_password
from repositories.rabit_mq import RabbitMQRepository
import logging


class UserServiceBase(ABC):
    @abstractmethod
    async def login_user(self, user_data):
        pass

    @abstractmethod
    async def create_user(self, user_data):
        pass


class UserService(UserServiceBase):
    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.jwt_repo = JWTTokenRepository()
        self.rabit_mq_repo = RabbitMQRepository()

    async def login_user(self, user_data: OAuth2PasswordRequestForm) -> Token:
        existing_user = await self.user_repo.verify_credentials(user_data)
        access = self.jwt_repo.create_access_token(existing_user.id)
        refresh = self.jwt_repo.create_refresh_token(existing_user.id)
        token = Token(access_token=access, refresh_token=refresh)
        return token

    async def create_user(self, user_data: UserCreate) -> ResponseUserForm:
        user_data.password = get_hashed_password(user_data.password)
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if not existing_user:
            new_user = await self.user_repo.create_user(user_data)
            access = self.jwt_repo.create_access_token(new_user.id)
            refresh = self.jwt_repo.create_refresh_token(new_user.id)
            token = Token(access_token=access, refresh_token=refresh)
            await self.rabit_mq_repo.publish(message={'email': 'user_data.email'},
                                             routing_key='notification_create_user')
            return ResponseUserForm(**user_data.dict(), id=new_user.id, token=token)
        else:
            raise HTTPException(status_code=400, detail="User with this email already exists")
