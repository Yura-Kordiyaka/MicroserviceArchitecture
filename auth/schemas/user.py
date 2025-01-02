from pydantic import BaseModel, EmailStr
from .token import Token


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class ResponseUserForm(UserBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class LoginForm(BaseModel):
    email: EmailStr
    password: str


class AuthForm(UserBase):
    password: str


class ResetPasswordForm(BaseModel):
    email: EmailStr


class ResetPasswordPasswordForm(BaseModel):
    password: str
    token: str


class SetPassword(BaseModel):
    password: str
