from abc import ABC, abstractmethod
from http.client import HTTPException

from config import settings
from datetime import timedelta, datetime
from jose import JWTError, jwt

class TokenBaseRepository(ABC):
    @abstractmethod
    def create_access_token(self, subject):
        pass

    @abstractmethod
    def create_refresh_token(self, subject):
        pass

    @abstractmethod
    def verify_access_token(self, subject):
        pass

    @abstractmethod
    def verify_refresh_token(self, subject):
        pass

class JWTTokenRepository(TokenBaseRepository):
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.token.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_MINUTES = settings.token.REFRESH_TOKEN_EXPIRE_MINUTES
    ALGORITHM = settings.token.ALGORITHM
    JWT_SECRET_KEY = settings.token.JWT_SECRET_KEY
    JWT_REFRESH_SECRET_KEY = settings.token.JWT_REFRESH_SECRET_KEY

    def create_access_token(self, subject):
        expires_delta = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self,subject):
        expires_delta = datetime.utcnow() + timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.JWT_REFRESH_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def verify_access_token(self, access_token):
            try:
                payload = jwt.decode(access_token, self.JWT_SECRET_KEY, algorithms=self.ALGORITHM)
                id: str = payload.get("sub")
                if id is None:
                    raise HTTPException("user is not anothorize")
                token_data = id
            except JWTError as e:
                print(e)
                raise HTTPException("user is not anothorize")
            return token_data


    def verify_refresh_token(self,refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.JWT_REFRESH_SECRET_KEY, algorithms=[self.ALGORITHM])
            id: str = payload.get("sub")
            if id is None:
                raise HTTPException("token is invalid")
            token_data = id
        except JWTError as e:
            raise HTTPException("token is invalid")
        return token_data