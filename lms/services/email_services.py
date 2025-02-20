from fastapi_mail import FastMail , ConnectionConfig , MessageSchema , MessageType

from lms.config.settings import Settings
from plyer import notification

settings = Settings()

config = ConnectionConfig(
        MAIL_FROM = settings.MAIL_FROM ,
        MAIL_PASSWORD = settings.MAIL_PASSWORD ,
        MAIL_PORT = settings.MAIL_PORT ,
        MAIL_STARTTLS = settings.MAIL_STARTTLS ,
        MAIL_USERNAME = settings.MAIL_USERNAME ,
        MAIL_SSL_TLS = settings.MAIL_SSL_TLS ,
        MAIL_SERVER = settings.MAIL_SERVER ,
        MAIL_FROM_NAME = settings.MAIL_FROM_NAME ,
        USE_CREDENTIALS = True
)

mail = FastMail(config)


class EmailServices :
    
    @staticmethod
    async def email_message(message: str , email: str , subject) :
        try :
            schema = MessageSchema(
                    recipients = [email] ,
                    subject = subject ,
                    body = message ,
                    subtype = MessageType.plain
            )
            await mail.send_message(schema)
            notification.notify(
                    title = 'Verify' ,
                    message = 'verification code sent to your email' ,
                    app_name = 'Verification' ,
                    timeout = 5)
        except Exception as e :
            print(f'An error occurred {e}')
            
        
    
