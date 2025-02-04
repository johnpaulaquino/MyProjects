from fastapi import (
    APIRouter,
    HTTPException,
    status, BackgroundTasks, Response, Request)
from starlette.responses import JSONResponse

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
async def create_account(user: SignUp,
                         address: AddressBase,
                         response : Response,
                         background_task : BackgroundTasks):
    global new_user
    # Hash the inputted password
    hashed_pass = Utility.hash_user_password(user.password)
    
    #to check whether the user is in the redis or not
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
            token = Utility.generate_access_token(data={
                    'email': existing_user['email']
            })
            response.set_cookie(key='verify_code_token',
                                value=token,
                                samesite='strict',
                                )
            code = Utility.generate_verification_code()
            await RedisUserCached.set_user_code_verification(code, existing_user['email'])
            return JSONResponse(
                status_code=200,
                content={'status': 'ok', 'message': 'It seems your email is not verified!'})
        
    
    #find the user via email
    is_user_exist = await UsersQueries.find_user_by_email(user.email)
        
    #check if the user is in the database
    if is_user_exist:
            #if it is in the db, then check if the user account is active or not
        if is_user_exist['is_active']:
            #if it is active, then raise an exception that says, email is already exist
            raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Email is already exist!'
            )
            #otherwise it will return response that says, It seems your email is not verified!
            #user just to need verify its email.
        else:
            token = Utility.generate_access_token(
                    data={
                            'email': is_user_exist['email']
                    })
            response.set_cookie(
                key='verify_code_token',
                value=token,
                samesite='strict',
                )
            code = Utility.generate_verification_code()
            await RedisUserCached.set_user_code_verification(code, is_user_exist['email'])
            return JSONResponse(
                    status_code=200,
                    content={'status': 'ok', 'message': 'It seems your email is not verified!'})
        
        #if user not found in db, then it will create a new user and its address.
        #and it will store in the db and redis db.
    to_str_b_day = user.b_day.isoformat()
    user_age = Utility.calculate_user_age(user.b_day)
    new_user = await UsersQueries.create_user(
                Users(
                        email=user.email,
                        password=hashed_pass,
                        name=user.name,
                        age=user_age,
                        b_day=to_str_b_day))
        

        #to store the user credentials in the redis
    await RedisUserCached.set_user_data(new_user['email'],new_user)
   
    user = UserInDB(**new_user)
    user_address = Address(
            user_id=user.id,
            municipality=address.municipality,
            city=address.city,
            country=address.country,
            postal_code=address.postal_code)
    
    token = Utility.generate_access_token(
            data={
                    'email': existing_user['email']
            })
    response.set_cookie(
        key='verify_code_token',
        value=token,
        samesite='strict',
        )
    code = Utility.generate_verification_code()
    await RedisUserCached.set_user_code_verification(code, existing_user['email'])
    return JSONResponse(
        status_code=201, content={
                'status': 'success', 'message':
                    'Successfully created account, please verify your account!'
        },
    headers={'Authorization' : f'Bearer {token}'})

async def resend_code(email : str):
    pass


@signup.post('')
async def verify_user_email(code : str, request : Request):
    try:
        token = request.cookies.get('verify_code_token')
        
        if not token:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail= {'message': 'Please signup first!'}
            )
        try:
            email = await Utility.decode_generated_token(token)
        except Exception as e:
            print(f'An error occurred {e}!')
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={'message': 'Token is expired, please signup again!'}
            )
        
        is_existing_code = await RedisUserCached.get_user_code_verification(email['email'])
        
        if not is_existing_code:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='It seems your verification code is expired, please re-send it!'
            )
        if code != is_existing_code:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Enter verification code again!'
            )
        
        await UsersQueries.activate_user(email['email'])
        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'message': 'Account successfully verified, please back to login!'}
        )
    except Exception as e:
        print(f'An error occurred {e}!')