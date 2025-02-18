from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    firstname: str
    lastname: str
    middle_name: str
    email: str


class UserSchemaSignup(BaseUserSchema):
    password: str


class UserSchemaInDB(BaseUserSchema):
    hash_password: str
