from fastapi import (APIRouter , BackgroundTasks , )
from sqlalchemy.exc import SQLAlchemyError

from lms.database.models.users import Users
from lms.schemas.user_schema import UserSchemaSignup
from lms.services.db_services.users_db_services import UserDbServices

signup = APIRouter(
        prefix = '/create-user' ,
        tags = ['Sign Up']
)


@signup.post('/', status_code = 200)
async def create_user_account(user_cred: UserSchemaSignup, background_task : BackgroundTasks) :
    try:
        
        return await UserDbServices.create_user(user_cred, background_task)
    except Exception as e:
        print(f'An error occurred {e}')
        raise e