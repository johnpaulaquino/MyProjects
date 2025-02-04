
from fastapi import APIRouter, Depends, HTTPException, status, Response
from starlette.responses import JSONResponse

from taskmanagement.cached.user_cached import RedisUserCached
from taskmanagement.database.db_operations.users_op import UsersQueries
from taskmanagement.pydantic_models.users_schema import Login, UserInDB
from fastapi.security import OAuth2PasswordRequestForm

from taskmanagement.utils.utility import Utility

auth = APIRouter(prefix='/auth')



@auth.post('')
async def user_authenticate(response : Response, form_data : OAuth2PasswordRequestForm = Depends(), ):
    """
    This method is for authentication of the user to get access in the data.
    :param response:
    :param form_data:
        is the data that the user inputted in the form.
    :return:
        access_token and the toke_type if the user are authenticated.
    """
    #Check whether the user is in the cache, otherwise get the data in the database.
    user = await RedisUserCached.get_user_by_email(form_data.username)
    if not user:
        user = await UsersQueries.find_user_by_email(form_data.username)
        if not user:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='User not found!',
                    headers={'WWW-Authenticate': 'Bearer'}
            )
        if not Utility.authenticate_user(user, form_data.password):
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Incorrect password, please try again',
                    headers={'WWW-Authenticate': 'Bearer'}
            )
        
        await RedisUserCached.set_user_data(user['email'],user)
        
    #This is to make an access token
    access_token = Utility.generate_access_token(data={
            'user_id': user['id'],
            'username' : user['name']
    })
    
    response.set_cookie(
            key='access_token',
            value=access_token,
    )
    return JSONResponse(
            content='Success',
            headers={'Authorization': access_token}
    )#{'status' : 'success', 'message' : 'Authentication successfully!'}