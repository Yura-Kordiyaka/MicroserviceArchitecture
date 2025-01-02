from abc import ABC, abstractmethod
from schemas.user import LoginForm
from db.conf.session import get_session
from db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException
from utils.password import get_hashed_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm


class UserBaseRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    async def get_user_by_email(self, email):
        pass

    @abstractmethod
    async def create_user(self, user_data):
        pass

    @abstractmethod
    async def update_user(self, user):
        pass

    #
    # @abstractmethod
    # async def delete_user(self, user_id):
    #     pass

    @abstractmethod
    async def verify_credentials(self, user_data):
        pass


class UserRepository(UserBaseRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id):
        existing_user = (await self.db.execute(select(User).filter(User.id == user_id))).scalars().first()
        if existing_user is None:
            raise HTTPException(status_code=404, detail='User not found')
        return existing_user

    async def get_user_by_email(self, email):
        existing_user = (await self.db.execute(select(User).filter(User.email == email))).scalars().first()
        return existing_user

    async def create_user(self, user_data):
        if isinstance(user_data, dict):
            new_user = User(**user_data)
        else:
            new_user = User(**user_data.dict())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def verify_credentials(self, user_data: OAuth2PasswordRequestForm):
        existing_user = await self.get_user_by_email(user_data.username)
        if existing_user:
            if verify_password(user_data.password, existing_user.password):
                return existing_user
            else:
                raise HTTPException(status_code=400, detail="Invalid password")
        raise HTTPException(status_code=404, detail="User not found")

    async def update_user(self, user):
        await self.db.commit()
        await self.db.refresh(user)
