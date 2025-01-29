from fastapi_mail import FastMail, ConnectionConfig,MessageSchema


config = ConnectionConfig(
        MAIL_FROM=''
)


mails = FastMail()



