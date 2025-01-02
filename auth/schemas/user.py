from pydantic import BaseModel, EmailStr
from typing import Optional
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


class GoogleAuthData(BaseModel):
    id: str
    email: str
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: Optional[str] = None

    class Config:
        orm_mode = True
