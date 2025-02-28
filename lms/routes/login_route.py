from fastapi import APIRouter , Depends , HTTPException , status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from lms.database.db_repository.user_repo import UserRepository
from lms.utils.auth_utils import AuthUtility

login = APIRouter(
        tags = ['Authentication'] ,
        prefix = '/auth'
)


@login.post('/token' , status_code = status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) :
    try :
        user_cred = await UserRepository.find_user_by_email(form_data.username)
        if not user_cred :
            raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED ,
                    detail = 'Username not found!' ,
                    headers = {'WWW-Authenticate' : 'Bearer'}
            )
        if not AuthUtility.authenticate_user(user_cred , form_data.password) :
            raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED ,
                    detail = 'Incorrect Password!' ,
                    headers = {'WWW-Authenticate' : 'Bearer'}
            )
        
        user_id = user_cred['id']
        role = user_cred['role']
        
        access_token = AuthUtility.generate_access_token(
                {'user_id'   : user_id ,
                 'user_role' : role})
        
        return {'access_token' : access_token ,
                'access_type'  : 'bearer'}
    except Exception as e :
        print(f'An error occurred {e}')
        raise e
