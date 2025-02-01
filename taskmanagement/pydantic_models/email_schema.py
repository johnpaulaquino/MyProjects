from pydantic import BaseModel, EmailStr
from fastapi_mail import MessageType

class EmailSchema(BaseModel):
    recipients : list[EmailStr] | EmailStr
    subject : str | int
