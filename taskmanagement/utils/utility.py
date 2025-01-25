from uuid import uuid4

from argon2.exceptions import Argon2Error
from jose import jwt
from datetime import timedelta, datetime, timezone
from taskmanagement.pydantic_models.settings import Settings
from contextlib import asynccontextmanager
from passlib.context import CryptContext

from taskmanagement.pydantic_models.users_model import UserInDB

contex_password = CryptContext(schemes=['argon2'], deprecated='auto')
settings = Settings()


class Utility:
    @staticmethod
    def generate_uuid() -> str:
        """
        
        :return:
            The uuid in a string
        """
        return str(uuid4())
    
    @staticmethod
    def generate_access_token(data: dict):
        """
        
        :param data:
            This is the data that will encode to the token
        :return:
            the token
        """
        to_encode = data.copy()
        
        to_encode.update({'exp': datetime.now(timezone.utc) +  timedelta(minutes=2)})
        token = jwt.encode(
                to_encode,
                key=settings.SECRET_KEY,
                algorithm=settings.ALGORITHM)
        
        return token
    
    @staticmethod
    def generate_refresh_access_token(data: dict, expires_timedelta: timedelta):
        """
            this is the refresh token, after the token has been expired
        :param data:
            This is the data that will encode in the token
        :param expires_timedelta:
            This is the expiration of the token
        :return:
            the encoded token
        """
        to_encode = data.copy()
        expires = (datetime.now(timezone.utc) + expires_timedelta
                   if expires_timedelta else timedelta(days=5))
        
        to_encode.update({'exp': expires})
        token = jwt.encode(
                to_encode,
                key=settings.SECRET_KEY,
                algorithm=settings.ALGORITHM)
        
        return token
    
    @staticmethod
    @asynccontextmanager
    async def lifespan(app):
        print(f'Server is starting at port {settings.PORT}...')
        yield
        print('Server has been shutdown.')
    
    @staticmethod
    def hash_user_password(plain_pass: str):
        if not plain_pass:
            return False
        
        return contex_password.hash(plain_pass)
    
    @staticmethod
    def verify_user_password(plain_pass, hashed_pass):
        try:
            return contex_password.verify(secret=plain_pass, hash=hashed_pass)
        
        except Argon2Error as e:
            print(f'An error occurred {e}!')
            return False
    
    @staticmethod
    def get_user_data(result_query: dict, email: str):
        return UserInDB(**result_query)
    
    @staticmethod
    def authenticate_user(result_query: dict, password: str):
        if not result_query:
            return False
        
        if not Utility.verify_user_password(
                plain_pass=password,
                hashed_pass=result_query['hash_password']):
            return False
        
        return True
