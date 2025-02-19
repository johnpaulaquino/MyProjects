import time
from contextlib import asynccontextmanager
from uuid import uuid4

from argon2.exceptions import Argon2Error
from plyer import notification

from lms.utils.email_sender import email_message

import pyotp
from lms.config.settings import Settings
from passlib.context import  CryptContext
settings = Settings()
password_cont = CryptContext(schemes = ['argon2'], deprecated = 'auto')
code_generator = pyotp.TOTP(pyotp.random_base32(), interval = 180)

class Utility:
    

    #to hash password
    @staticmethod
    def hash_plain_password(plain_password : str):
        #hash the password
        return password_cont.hash(secret = plain_password)

    #to verify user password
    @staticmethod
    def verify_hashed_password(plain_password, hashed_password):
        try:
            return password_cont.verify(secret = plain_password,hash = hashed_password)
        except Argon2Error as e:
            print(f'An error occurred {e}')
            return False
    
    
    #to generate uuid
    @staticmethod
    def generate_uuid() -> str:
        return str(uuid4())
    
    #for lifespan of an app
    @staticmethod
    @asynccontextmanager
    async def create_lifespan(app):
        print(f'Server is starting at port {settings.PORT}...')
        yield
        print(f'Server is shutting down..')
    
    @staticmethod
    async def send_email(email, message, subject):
        try:
            time_start = time.time()
            notification.notify(
                    title='verification',
                    message= 'Email is sending...',
                    timeout= 1
            )
            await email_message(email = [email],message = message,subject = subject)
            
            notification.notify(
                    title = 'verification' ,
                    message = 'verification code sent to your email' ,
                    timeout = 5
            )
        except Exception as e:
            print(f'An error occurred {e}')
    
    
    @staticmethod
    def generate_verification_code():
        return code_generator.now()
        
    @staticmethod
    def verify_code_verification(code : str):
        return code_generator.verify(code)

    
    
