from fastapi import (APIRouter , BackgroundTasks , status)

from lms.schemas.user_schema import UserSchemaSignup
from lms.services.auth_services import AuthServices

signup = APIRouter(
        prefix = '/create-user' ,
        tags = ['Sign Up']
)


@signup.post('/', status_code = status.HTTP_200_OK)
async def create_user_account(user_cred: UserSchemaSignup, background_task : BackgroundTasks) :
    try:
        
        return await AuthServices.create_user_account(user_cred, background_task)
    except Exception as e:
        raise e

@signup.post('/verify', status_code = status.HTTP_201_CREATED)
async def verify_user(email : str, code : str):
    try:
        return await AuthServices.verify_user_account(email = email, code= code)
    except Exception as e:
        raise e
    
@signup.get('/re-send/verification-code')
async def re_send_verification_code(email : str, background_task: BackgroundTasks):
    try:
        return await AuthServices.re_send_code(email, background_task)
    except Exception as e:
        raise e