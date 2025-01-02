from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from db.conf.session import get_session
from schemas.user import ResponseUserForm, LoginForm, UserCreate, ResetPasswordForm, ResetPasswordPasswordForm, \
    SetPassword
from schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from services.user_service import UserService, get_authenticated_user
from services.auth_service import AuthService
from services.email_service import EmailService
from services.reset_password import ResetPasswordService

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/sign_up", response_model=ResponseUserForm, status_code=status.HTTP_201_CREATED)
async def sign_up(user: UserCreate, db: AsyncSession = Depends(get_session)):
    user_service = AuthService(db)
    user = await user_service.create_user(user)
    return user


@user_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(user: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user_service = AuthService(db)
    user = await user_service.login_user(user)
    return user


@user_router.patch('/confirm_email', status_code=status.HTTP_200_OK)
async def confirm_email(token: str, db: AsyncSession = Depends(get_session)):
    user_service = EmailService(db)
    response = await user_service.confirm_mail(token)
    return response


@user_router.post('/send_reset_token', status_code=status.HTTP_200_OK)
async def send_reset_token(email: ResetPasswordForm, db: AsyncSession = Depends(get_session)):
    reset_token_service = ResetPasswordService(db)
    result = await reset_token_service.send_reset_token(email)
    return result


@user_router.post('/confirm-reset-token', status_code=status.HTTP_200_OK)
async def set_new_password(token: str):
    user_service = ResetPasswordService()
    result = await user_service.confirm_reset_token(token)
    return result


@user_router.post('/reset-password', status_code=status.HTTP_200_OK)
async def reset_password(password: ResetPasswordPasswordForm, db: AsyncSession = Depends(get_session)):
    user_service = ResetPasswordService(db)
    result = await user_service.reset_password(password)
    return result


@user_router.post('/set-password', status_code=status.HTTP_200_OK)
async def set_new_password(password_form: SetPassword, db: AsyncSession = Depends(get_session),
                           user: ResponseUserForm = Depends(get_authenticated_user)):
    user_service = ResetPasswordService(db)
    result = await user_service.set_password(password_form, user)
    return result


@user_router.get('/info', summary='Get details of currently logged in user')
async def get_me(token: ResponseUserForm = Depends(get_authenticated_user)):
    return token
