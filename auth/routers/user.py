from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from db.conf.session import get_session
from schemas.user import ResponseUserForm,LoginForm,UserCreate
from schemas.token import Token
from utils.auth import login_user, get_current_user
import crud.user as crud_user
from fastapi.security import OAuth2PasswordRequestForm
from services.user import UserService
user_router = APIRouter(prefix="/user", tags=["user"])



@user_router.post("/sign_up", response_model=ResponseUserForm, status_code=status.HTTP_201_CREATED)
async def sign_up(user: UserCreate, db: AsyncSession = Depends(get_session)):
    user_service = UserService(db)
    user = await user_service.create_user(user)
    return user


@user_router.post("/login",response_model=Token, status_code=status.HTTP_200_OK)
async def login(user: OAuth2PasswordRequestForm  = Depends(), db: AsyncSession = Depends(get_session)):
    user_service = UserService(db)
    user = await user_service.login_user(user)
    return user


@user_router.get('/info', summary='Get details of currently logged in user', response_model=ResponseUserForm)
async def get_me(token: str = Depends(get_current_user)):
    return token

