from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from enum import Enum

class IsActive(Enum):
    TRUE : int = 1
    FALSE : int = 0

# This is the base user
class BaseUser(BaseModel):
    email: EmailStr
   


# inherit the attributes of base user
class SignUp(BaseUser):
    password: str
    name : str
    age : int
    b_day : str

class Login(BaseUser):
    password : str
#This will be the response output after signing up
class UserInDB(BaseUser):
    id: str
    name: str
    hash_password : str
    age : int
    b_day : str
    is_active: int = IsActive.TRUE
    