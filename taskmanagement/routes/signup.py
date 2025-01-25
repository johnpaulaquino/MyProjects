from fastapi import (
    APIRouter,
    HTTPException,
    status, )

from taskmanagement.pydantic_models.users_model import SignUp
from taskmanagement.database.db_tables.users import Users
from taskmanagement.database.db_operations.users_op import UsersQueries
from taskmanagement.utils.utility import Utility

signup = APIRouter(
        prefix='/signup',
        tags=['Signup'],
)


@signup.post('', status_code=201)
async def create_account(user: SignUp):
    hashed_pass = Utility.hash_user_password(user.password)
    new_user = await UsersQueries.create_user(
            Users(
                    email=user.email,
                    password=hashed_pass,
                    name=user.name,
                    age=user.age,
                    b_day=user.b_day))

    if not new_user:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email is already exist, try another email.'
        )
    
    return {
            'status': 'success', 'message':
                'Successfully created account!'
    }
