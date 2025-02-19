import asyncio

from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType

from lms.config.settings import Settings
from pydantic import SecretStr, EmailStr


settings = Settings()

config = ConnectionConfig(
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_PORT= settings.MAIL_PORT,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        USE_CREDENTIALS=True
)

mail = FastMail(config)
async def email_message(message: str , email: list , subject):

    schema = MessageSchema(
        recipients = email ,
        subject = subject ,
        body = message ,
        subtype = MessageType.plain
    )
    
    await mail.send_message(schema)
    