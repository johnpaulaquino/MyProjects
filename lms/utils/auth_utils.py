
from argon2.exceptions import Argon2Error

from lms.config.settings import Settings
from passlib.context import  CryptContext

settings = Settings()
password_cont = CryptContext(schemes = ['argon2'], deprecated = 'auto')


class AuthUtility:
    

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
