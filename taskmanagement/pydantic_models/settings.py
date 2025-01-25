
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    #For DATABASE
    DB_URL : str
    #for access token
    SECRET_KEY : str
    ALGORITHM : str
    EXPIRED_ACCESS_TOKEN : int
    PORT : str
