from fastapi import APIRouter, Depends, HTTPException, status

from taskmanagement.database.db_operations.users_op import UsersQueries
from taskmanagement.pydantic_models.users_model import Login
from fastapi.security import OAuth2PasswordRequestForm

from taskmanagement.utils.utility import Utility

auth = APIRouter(prefix='/auth')



@auth.post('')
async def user_authenticate(form_data : OAuth2PasswordRequestForm = Depends()):
    user = await UsersQueries.find_user_by_email(form_data.username)
    print(user)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User not found!',
                headers= {'WWW-Authenticate' : 'Bearer'}
        )
   
    if not Utility.authenticate_user(user, form_data.password):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect password, please try again',
                headers={'WWW-Authenticate': 'Bearer'}
        )
    
    access_token = Utility.generate_access_token(data={
            'user_id': user['id'],
            'username' : user['name']
    })
    
    return {'access_token' : access_token, 'access_type' : 'bearer'}