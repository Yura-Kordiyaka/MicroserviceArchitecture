from fastapi import HTTPException,Depends
from repositories.user import UserRepository
from repositories.token import JWTTokenRepository
import logging

class EmailService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.jwt_repo = JWTTokenRepository()

    async def confirm_mail(self, token: str) -> int:
        user_id = self.jwt_repo.verify_access_token(token)
        if user_id:
            user = await self.user_repo.get_user_by_id(int(user_id))
            user.confirm_email = True
            await self.user_repo.update_user(user)
            return 200
        else:
            raise HTTPException(status_code=404, detail="Confirmation token not found or expired")


