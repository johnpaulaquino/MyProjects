import asyncio
from datetime import datetime
from fastapi import (
    APIRouter,
    HTTPException,
    status, BackgroundTasks, )

from taskmanagement.cached.user_cached import RedisUserCached
from taskmanagement.database.db_tables.address import Address
from taskmanagement.pydantic_models.address_schema import AddressBase
from taskmanagement.pydantic_models.users_schema import SignUp, UserInDB
from taskmanagement.database.db_tables.users import Users
from taskmanagement.database.db_operations.users_op import UsersQueries
from taskmanagement.utils.utility import Utility

signup = APIRouter(
        prefix='/signup',
        tags=['Signup'],
)


@signup.post('', status_code=201)
async def create_account(user: SignUp, address: AddressBase):
    hashed_pass = Utility.hash_user_password(user.password)
    
    find_user_in_redis = await RedisUserCached.get_user_by_email(user.email)
    new_user = find_user_in_redis
    
    if new_user:
        if new_user['is_active']:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Email is already exist!'
            )
    
    if not find_user_in_redis:
        
        is_user_exist = await UsersQueries.find_user_by_email(user.email)
        
        if is_user_exist:
            if is_user_exist['is_active']:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Email is already exist!'
                )
            else:
                return {'status': 'ok', 'message': 'Please verify your email'}
        
        db_user = await UsersQueries.create_user(
                Users(
                        email=user.email,
                        password=hashed_pass,
                        name=user.name,
                        age=user.age,
                        b_day=user.b_day))
        
        # await RedisUserCached.set_user_data(new_user['email'],new_user)
    
    # user = UserInDB(**new_user)
    # user_address = Address(
    #         user_id=user.id,
    #         municipality=address.municipality,
    #         city=address.city,
    #         country=address.country,
    #         postal_code=address.postal_code)
    #
    # await UsersQueries.create_user_address(user_address)
    #
    return {
            'status': 'success', 'message':
                'Successfully created account!'
    }
