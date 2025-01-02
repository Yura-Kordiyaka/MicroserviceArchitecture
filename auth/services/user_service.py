from fastapi import HTTPException,Depends
from repositories.user import UserRepository
from repositories.token import JWTTokenRepository
from schemas.user import UserCreate, ResponseUserForm
from repositories.rabit_mq import RabbitMQRepository
from repositories.redis_client import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from db.conf.session import get_session
from db.models.user import User
from fastapi.security import OAuth2PasswordBearer
import logging

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/api/v1/user/login",
    scheme_name="Bearer"
)
class UserService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.jwt_repo = JWTTokenRepository()
        self.rabit_mq_repo = RabbitMQRepository()
        self.redis_client = RedisClient()

    async def get_current_user(self, token: str) -> User:
        user_id = self.jwt_repo.verify_access_token(token)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        user = await self.user_repo.get_user_by_id(int(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return ResponseUserForm.from_orm(user)

    async def get_current_user_service(self, token: str = Depends(oauth2_scheme)) -> User:
        return await self.get_current_user(token)


async def get_authenticated_user(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
) -> User:
    auth_user = UserService(db)
    return await auth_user.get_current_user(token)