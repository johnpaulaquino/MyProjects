from pydantic import BaseModel, EmailStr
from fastapi_mail import MessageType

class EmailSchema(BaseModel):
   email: list[EmailStr]
