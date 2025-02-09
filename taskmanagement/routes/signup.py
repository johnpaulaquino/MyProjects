from fastapi import (APIRouter, BackgroundTasks, HTTPException, Request, Response, status)
from fastapi.params import Depends
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlalchemy.util import await_only

from taskmanagement.cached.user_cached import RedisUserCached
from taskmanagement.database.db_operations.adress_op import AddressQueries
from taskmanagement.database.db_operations.users_op import UsersQueries
from taskmanagement.database.db_tables.address import Address
from taskmanagement.database.db_tables.users import Users
from taskmanagement.pydantic_models.address_schema import AddressBase
from taskmanagement.pydantic_models.users_schema import SignUp, UserInDB
from taskmanagement.utils.utility import Utility

signup = APIRouter(
        prefix='/signup',
        tags=['Signup'],
)


@signup.post('', status_code=200)
async def create_account(
        response: Response,
        user: SignUp,
        address: AddressBase,
        background_task: BackgroundTasks):
    global new_user
    # Hash the inputted password
    hashed_pass = Utility.hash_user_password(user.password)
    
    # to check whether the user is in the redis or not
    find_user_in_redis = await RedisUserCached.get_user_by_email(user.email)
    
    existing_user = find_user_in_redis
    # check if is not exists in the redis, then it will query in the db
    if existing_user:
        if existing_user['is_active']:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Email is already exist!'
            )
        else:
            token = Utility.generate_access_token(data={'email': existing_user['email']})
            response.set_cookie(
                    key='verify_code_token',
                    value=token)
            code = Utility.generate_verification_code()
            await RedisUserCached.set_user_code_verification(code, existing_user['email'])
            
            return {'status' : 'ok',
                            'message': 'It seems your email is not verified!'}

    
    # find the user via email
    is_user_exist = await UsersQueries.find_user_by_email(user.email)
    # check if the user is in the database
    if is_user_exist:
        # if it is in the db, then check if the user account is active or not
        if is_user_exist['is_active']:
            # if it is active, then raise an exception that says, email is already exist
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Email is already exist!'
            )
            # otherwise it will return response that says, It seems your email is not verified!
            # user just to need verify its email.
        else:
            code = Utility.generate_verification_code()
            await RedisUserCached.set_user_code_verification(code, is_user_exist['email'])
            token = Utility.generate_access_token(
                    data={
                            'email': is_user_exist['email'],
                            'id' : is_user_exist['id']
                    })
            
            response.set_cookie(
                    key='verify_code_token',
                    value=token)
            
            return {'status': 'ok', 'message': 'It seems your email is not verified!'},
            
            # if user not found in db, then it will create a new user and its address.
            # and it will store in the db and redis db.
    to_str_b_day = user.b_day.isoformat()
    user_age = Utility.calculate_user_age(user.b_day)
    new_user = await UsersQueries.create_user(
            Users(
                    email=user.email,
                    password=hashed_pass,
                    name=user.name,
                    age=user_age,
                    b_day=to_str_b_day))
    
    # to store the user credentials in the redis
    user_address = Address(
            user_id=new_user['id'],
            municipality=address.municipality,
            city=address.city,
            country=address.country,
            postal_code=address.postal_code)
    
    print('hey')
    address_result = await AddressQueries.add_address(user_address, new_user['id'])
    del address_result['user_id']
    user_full_info = new_user.copy()
    user_full_info.update({'address': address_result})
    await RedisUserCached.set_user_data(new_user['email'], new_user)
    code = Utility.generate_verification_code()
    await RedisUserCached.set_user_code_verification(code, new_user['email'])
    
    code_token = Utility.generate_access_token(
            data={
                    'email': new_user['email']
            })
    response.set_cookie(
            key='verify_code_token',
            value=code_token,
            httponly=True)
    response.status_code = 201
    background_task.add_task(Utility.email_message, code, [new_user['email']], 'Sample')
    return {
                    'status': 'success', 'message':
                        'Please check your email to verify your account!'
            }


@signup.get('/resend-code')
async def resend_code(request: Request, background_task: BackgroundTasks):
    try:
        token = request.cookies.get('verify_code_token')
        if not token:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Please signup first!'
            )
        verification_code = Utility.generate_verification_code()
        email = Utility.decode_generated_token(token)
        await RedisUserCached.set_user_code_verification(verification_code, email['email'])
        background_task.add_task(Utility.email_message, verification_code, [email['email']], 'Sample')
        return {'message': 'verification code is sent to your email!'}
    except Exception as e:
        print(f'An error occurred {e}!')
        raise e


@signup.post('/verify-email', status_code=status.HTTP_201_CREATED)
async def verify_user_email(code: str, request: Request):
    try:
        token = request.cookies.get('verify_code_token')
        if not token:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Please signup first!'
            )
        email = Utility.decode_generated_token(token)
    except Exception as e:
        print(f'An error occurred {e}!')
        raise e
    
    is_existing_code = await RedisUserCached.get_user_code_verification(email['email'])
    
    if not is_existing_code:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='It seems your verification code is expired, please re-send it!'
        )
    if Utility.verify_code(code):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Enter verification code again!'
        )
    
    update_user = await UsersQueries.activate_user(email['email'])
    await RedisUserCached.set_user_data(update_user['email'], update_user)
    
    return {'message': 'Account successfully verified, please back to login!'}



