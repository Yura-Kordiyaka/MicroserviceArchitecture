from pydantic import BaseModel, EmailStr
from .token import Token
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class ResponseUserForm(UserBase):
    pass

class LoginForm(BaseModel):
    email: EmailStr
    password: str

class AuthForm(UserBase):
    password: str
