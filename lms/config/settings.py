from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import SecretStr, EmailStr


load_dotenv()

class Settings(BaseSettings):
    DB_URL : str
    PORT : int
    
    #For JWT
    JWT_ALGORITHM : str
    JWT_REFRESH_ACCESS_KEY: int
    JWT_KEY : str
    
    MAIL_PASSWORD: SecretStr
    MAIL_FROM: EmailStr
    MAIL_PORT : int
    MAIL_USERNAME : str
    MAIL_STARTTLS : bool
    MAIL_SSL_TLS : bool
    USE_CREDENTIALS : bool
    VALIDATE_CERTS : bool
    MAIL_FROM_NAME : str
    MAIL_SERVER : str
    
    class Config:
        env_file = SettingsConfigDict(
            env_file = '.env',
            env_file_encoding = 'utf-8'
            
        )