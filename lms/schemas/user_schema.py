from pydantic import (
    BaseModel,
    EmailStr ,
)

from enum import Enum


class BaseUserSchema(BaseModel) :
    firstname: str = 'John'
    middle_name: str = 'Chicago'
    lastname: str = 'Doe'
    email: EmailStr
    role: str = 'user'


class UserSchemaSignup(BaseUserSchema) :
    password: str = 'samplepassword'


class UserSchemaInDB(BaseUserSchema) :
    hash_password: str
