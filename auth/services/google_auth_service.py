from abc import ABC, abstractmethod
from urllib.request import Request

from fastapi import HTTPException, Depends
from repositories.user import UserRepository
from repositories.token import JWTTokenRepository
from schemas.user import GoogleAuthData
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import Token
from utils.password import get_hashed_password, verify_password
from repositories.rabit_mq import RabbitMQRepository
from repositories.redis_client import RedisClient
from config import settings
from fastapi.responses import RedirectResponse
import requests


class GoogleAuthService:
    def __init__(self, db=None):
        if db:
            self.user_repo = UserRepository(db)
        self.jwt_repo = JWTTokenRepository()
        self.rabit_mq_repo = RabbitMQRepository()

    @staticmethod
    async def get_google_url():
        return {
            "url": f"https://accounts.google.com/o/oauth2/auth"
                   f"?response_type=code&client_id={settings.google_settings.GOOGLE_CLIENT_ID}"
                   f"&redirect_uri={settings.google_settings.GOOGLE_REDIRECT_URL}"
                   f"&scope=openid%20profile%20email&access_type=offline"
        }

    @staticmethod
    async def get_google_token(code: str) -> RedirectResponse:
        token_url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": code,
            "client_id": settings.google_settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.google_settings.GOOGLE_SECRET_ID,
            "redirect_uri": settings.google_settings.GOOGLE_REDIRECT_URL,
            "grant_type": "authorization_code",
        }
        response = requests.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        access_token = response.json().get("access_token")
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                                 headers={"Authorization": f"Bearer {access_token}"})
        payload = user_info.json()
        print(f'user data is: {payload}')
        return RedirectResponse(url=f'http://localhost:8002/dashboard?token={access_token}')

    async def google_auth(self, data: GoogleAuthData) -> Token:
        try:
            email = data.email
            user = await self.user_repo.get_user_by_email(email)

            if not user:
                user_data = {
                    "email": email,
                    "first_name": data.given_name,
                    "last_name": data.family_name,
                    "confirm_email": data.verified_email
                }
                user = await self.user_repo.create_user(user_data)

            access_token = self.jwt_repo.create_access_token(user.id)
            refresh_token = self.jwt_repo.create_refresh_token(user.id)

            if not data.verified_email and not user:
                confirm_url = f"http://yourfrontenddomain.com/confirm_email?token={access_token}"
                subject = 'Confirm your email'
                body = confirm_url
                await self.rabit_mq_repo.publish(message={
                    'email': data.email,
                    'subject': subject,
                    'body': body
                }, routing_key=settings.queue_settings.user_creation_queue)

            return Token(access_token=access_token, refresh_token=refresh_token)

        except KeyError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {str(e)}"
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred during Google authentication: {str(e)}"
            ) from e

    # if email:
    #     user = await self.user_repo.get_user_by_email(email)
    #     if not user:
    #         user.create_user()
    #

    # async def create_user(self, user_data: UserCreate) -> ResponseUserForm:
    #     user_data.password = get_hashed_password(user_data.password)
    #     existing_user = await self.user_repo.get_user_by_email(user_data.email)
    #     if not existing_user:
    #         new_user = await self.user_repo.create_user(user_data)
    #         access = self.jwt_repo.create_access_token(new_user.id)
    #         refresh = self.jwt_repo.create_refresh_token(new_user.id)
    #         confirm_url = f"http://yourfrontenddomain.com/confirm_email?token={access}"
    #         token = Token(access_token=access, refresh_token=refresh)
    #         subject = 'Confirm your email'
    #         body = confirm_url
    #         await self.rabit_mq_repo.publish(message={
    #             'email': user_data.email,
    #             'subject': subject,
    #             'body': body
    #         }, routing_key=settings.queue_settings.user_creation_queue)
    #         return ResponseUserForm(**user_data.dict(), id=new_user.id, token=token)
    #     else:
    #         raise HTTPException(status_code=400, detail="User with this email already exists")
