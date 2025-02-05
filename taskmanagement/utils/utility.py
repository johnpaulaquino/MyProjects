import asyncio
from uuid import uuid4

from argon2.exceptions import Argon2Error
from fastapi_mail import MessageSchema, MessageType,FastMail
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import timedelta, datetime, timezone, date

from taskmanagement.pydantic_models.email_schema import EmailSchema
from taskmanagement.pydantic_models.settings import Settings
from contextlib import asynccontextmanager
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from starlette.responses import JSONResponse
from taskmanagement.pydantic_models.users_schema import TokenData, UserInDB
import pyotp
from taskmanagement.utils.mail import config

contex_password = CryptContext(schemes=['argon2'], deprecated='auto')
settings = Settings()

generate_code = pyotp.TOTP(pyotp.random_base32(), interval=60)


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
        This function is to generate an access token that will store the data of the user
        
        :param data:
            This is the data that will encode to the token
        :return:
            the token
        """
        to_encode = data.copy()
        
        to_encode.update({'exp': datetime.now(timezone.utc) + timedelta(minutes=2)})
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
    def decode_generated_token(token: str):
        """
        Decodes a given JWT token and extracts its payload.

        This function attempts to decode a JSON Web Token (JWT) using the predefined secret key
        and algorithm. If successful, it returns the decoded payload as a dictionary.
        If the token is invalid or expired, it returns `None`.

        :param token: The JWT token as a string.
        :return:
            - A dictionary containing the decoded token data if valid.
            - None if the token is invalid, expired, or if an error occurs.

        :raises jwt.ExpiredSignatureError: If the token has expired.
        :raises jwt.InvalidTokenError: If the token is malformed or invalid.
        """
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            
            if not payload:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Invalid credentials!',
                        headers={'WWW-Authenticate': 'Bearer'}
                )
        
        except JWTError :
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Token is expired, please sign up again!'
            )
        if not payload:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid credentials!',
                    headers={'WWW-Authenticate': 'Bearer'}
            )
        
        return payload
    
    @staticmethod
    @asynccontextmanager
    async def lifespan(app):
        """
        Manages the startup and shutdown lifecycle of the FastAPI application.

        This method is a FastAPI lifespan function that performs:
        - **Startup Tasks:** Executes actions before the application starts (e.g., DB connections, caching setup).
        - **Shutdown Tasks:** Executes actions after the application is shutting down (e.g., closing connections, cleaning up resources).

        :param app: The FastAPI application instance.
        :yield: Nothing (used for setup/teardown purposes).
        """
        
        # 🟢 Server startup logic (e.g., connecting to DB, initializing caches)
        print(f'Server is starting at port {settings.PORT}...')
        yield
        print('Server has been shutdown.')
    
    @staticmethod
    def hash_user_password(plain_pass: str):
        """
        to hash the user password, to make it secure.
        :param plain_pass: the user input
        :return: False, if the plain pass is None, otherwise return the string
        hashed password.
        """
        if not plain_pass:
            return False
        
        return contex_password.hash(plain_pass)
    
    @staticmethod
    def verify_user_password(plain_pass, hashed_pass):
        """
        it checks if the user input in a readable form match to the hashed
        password that are stored in the database.
        :param plain_pass: is the user input in a readable form
        :param hashed_pass: is the hashed password that are stored in the datebase
        :return: True if both the same, otherwise, False
        """
        
        try:
            return contex_password.verify(secret=plain_pass, hash=hashed_pass)
        
        except Argon2Error as e:
            print(f'An error occurred {e}!')
            return False
    
    @staticmethod
    def get_user_data(result_query: dict):
        """
        its simply get the user data
        :param result_query: where the data fetched
        :return: the user object if there's a data in the result query, otherwise
        :return: False
        """
        if not result_query:
            return False
        return UserInDB(**result_query)
    
    @staticmethod
    def authenticate_user(result_query: dict, password: str):
        """
        to authenticate the user, just simply, get the user_data in the
        query, it's either in the database or in the redis.
        
        :param result_query:  is the data that we fetch in the database or in
        the redis database.
        :param password: is the user credentials, that will use to verify if
        the data belongs to him/her.
        :return: True if authenticated, otherwise False
        """
        
        if not result_query:
            return False
        
        if not Utility.verify_user_password(
                plain_pass=password,
                hashed_pass=result_query['hash_password']):
            return False
        
        return True
    
    @staticmethod
    def calculate_user_age(b_day: date):
        """
        to get the age of the use. first, need to subtract the year today and
        the birthday year, after that, just, check the today's month if is greater
        than or equal to the b_day month. if it is greater than or equal, it will
        check the today's date if it is less than to the b_day day, if yes, then simply
        subtract the age, because the user is not yet celebrating the user, otherwise
        just remain it. Lastly, if today's month is less than to the b_day, just simply
        subtract it, because, it says that user is not yet celebrating its birthday.
        
        :param b_day: the birthday of the user, to calculate the ag.
        :return: the age of the user
        """
        
        # check if the b_day is None then, return False, otherwise proceed to calculation
        if not b_day:
            return False
        
        # get the current date
        today_date = date.today()
        # Calculate age by subtracting today year and b day year
        calculated_age = today_date.year - b_day.year
        
        # check if today month is greater than or equal to  the b_day month,
        # If yes,
        if today_date.month >= b_day.month:
            # then it will check today's date if less than to the
            # b_day date, then subtract the age by one
            if today_date.day < b_day.day:
                calculated_age -= 1
            else:
                # otherwise remain the age
                pass
        else:
            # otherwise subtract the age by one
            calculated_age -= 1
        
        return calculated_age
    
    @staticmethod
    def generate_verification_code():
        code = generate_code.now()
        return code
    
    @staticmethod
    def verify_code(code: str):
        
        if not generate_code.verify(code):
            return False
        
        return True
    
    @staticmethod
    async def email_message(message: str, email : list, subject):
        mail = FastMail(config)
        schema = MessageSchema(
                recipients=email,
                subject=subject,
                body=message,
                subtype=MessageType.plain
        )
        
        await mail.send_message(schema)