import asyncio
from datetime import datetime
from fastapi import (
    APIRouter,
    HTTPException,
    status, )

from taskmanagement.cached.user_cached import RedisUserCached
from taskmanagement.database.db_tables.address import Address
from taskmanagement.pydantic_models.address_model import AddressBase
from taskmanagement.pydantic_models.users_model import SignUp
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
    new_user = await UsersQueries.create_user(
            Users(
                    email=user.email,
                    password=hashed_pass,
                    name=user.name,
                    age=user.age,
                    b_day=str(user.b_day)))

    if not new_user:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email is already exist, try another email.'
        )
    
    user_address = Address(
            user_id=new_user['id'],
            municipality=address.municipality,
            city=address.city,
            country=address.country,
            postal_code=address.postal_code)
    
    await UsersQueries.create_user_address(user_address)

    return {
            'status': 'success', 'message':
                'Successfully created account!'
    }
