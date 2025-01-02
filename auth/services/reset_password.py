from fastapi import HTTPException, Depends

from db.models.user import User
from repositories.user import UserRepository
from repositories.token import JWTTokenRepository
from utils.password import get_hashed_password
from schemas.user import ResponseUserForm, ResetPasswordForm, ResetPasswordPasswordForm, SetPassword
from repositories.rabit_mq import RabbitMQRepository
import secrets
import string
from repositories.redis_client import RedisClient
from config import settings
from fastapi.responses import JSONResponse


class ResetPasswordService:
    def __init__(self, db=None):
        if db:
            self.user_repo = UserRepository(db)
        self.rabit_mq_repo = RabbitMQRepository()
        self.redis_client = RedisClient()

    async def send_reset_token(self, user_email: ResetPasswordForm) -> int:
        characters = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(characters) for _ in range(6))
        user = await self.user_repo.get_user_by_email(user_email.email)
        if user is None:
            raise HTTPException(status_code=404, detail="User does not exist")
        await self.redis_client.save_data_to_redis(f'reset_token_{random_string}', f'{user.id}', 60 * 10)
        await self.rabit_mq_repo.publish(message={
            'email': user.email,
            'subject': 'Reset Password',
            'body': random_string
        }, routing_key=settings.queue_settings.reset_password_queue)
        return JSONResponse(status_code=200, content={"message": "Token was sent to user"})

    async def confirm_reset_token(self, token: str) -> int:
        token_reset_pass = await self.redis_client.get_data_from_redis(f'reset_token_{token}')
        if not token_reset_pass:
            return HTTPException(status_code=200, detail='token is expired')
        return JSONResponse(status_code=200, content={"message": "Token is valid"})

    async def reset_password(self, new_password_form: ResetPasswordPasswordForm) -> int:
        token_reset_pass = await self.redis_client.get_data_from_redis(f'reset_token_{new_password_form.token}')
        user = await self.user_repo.get_user_by_id(int(token_reset_pass))
        if user is None:
            return HTTPException(status_code=404, detail='User not found')
        user.password = get_hashed_password(new_password_form.password)
        await self.user_repo.update_user(user)
        return JSONResponse(status_code=201, content={"message": "password updated"})

    async def set_password(self, password_form: SetPassword, user: ResponseUserForm) -> JSONResponse:
        user = await self.user_repo.get_user_by_id(user.id)
        if user is None:
            return HTTPException(status_code=404, detail='User not found')
        user.password = get_hashed_password(password_form.password)
        await self.user_repo.update_user(user)
        return JSONResponse(status_code=201, content={"message": "password updated"})
