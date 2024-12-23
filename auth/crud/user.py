import schemas.user
import schemas.token
from db.models.user import User
from fastapi import Depends, HTTPException
from db.conf.session import get_session
from schemas.user import ResponseUserForm,UserCreate
from utils.auth import create_access_token, create_refresh_token, get_hashed_password
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(db: Depends(get_session), user_in: UserCreate) -> ResponseUserForm:
    user_in.password = get_hashed_password(user_in.password)
    existing_user = await db.execute(select(User).filter(
        (User.email == user_in.email)))
    existing_user = existing_user.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this notification already exists")
    user = User(**user_in.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    access = await create_access_token(user.id)
    refresh = await create_refresh_token(user.id)
    token = schemas.token.Token(access_token=access, refresh_token=refresh)
    return ResponseUserForm(**user_in.dict(), id=user.id, token=token)

