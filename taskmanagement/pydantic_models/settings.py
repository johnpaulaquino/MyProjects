
from dotenv import load_dotenv
from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    #For DATABASE
    DB_URL : str
    
    
    #port for app
    PORT : int = 8000
    
    #for access token
    SECRET_KEY : str
    ALGORITHM : str
    EXPIRED_ACCESS_TOKEN : int
    
    # For Email credentials
    MAIL_FROM : EmailStr
    MAIL_PASSWORD : SecretStr
    MAIL_USERNAME : str
    MAIL_STARTTLS : bool
    MAIL_SSL_TLS : bool
    USE_CREDENTIALS : bool
    VALIDATE_CERTS : bool
    MAIL_PORT : int
    MAIL_SERVER : str
    MAIL_FROM_NAME: str
settings = Settings()
