from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError,ExpiredSignatureError

from lms.database.db_repository.user_repo import UserRepository

from lms.config.settings import Settings
from fastapi import HTTPException, status

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/auth/token')
class Dependencies:
    @staticmethod
    async def get_current_user(token : str = Depends(oauth2_scheme)) :
        try :
            print(token)
            payload = jwt.decode(token , settings.JWT_KEY , algorithms = [settings.JWT_ALGORITHM])
            if not payload:
                raise HTTPException(
                        status_code = status.HTTP_401_UNAUTHORIZED,
                        detail = 'Could not validate credentials',
                        headers = {'WWW-Authenticate' : 'Bearer'}
                )
            user_id = payload.get('user_id')
            if not user_id:
                raise HTTPException(
                        status_code = status.HTTP_401_UNAUTHORIZED ,
                        detail = 'Could not validate credentials!' ,
                        headers = {'WWW-Authenticate' : 'Bearer'}
                )
            curr_user = await UserRepository.find_user_by_user_id(user_id)
            
            if not curr_user:
                raise HTTPException(
                        status_code = status.HTTP_401_UNAUTHORIZED ,
                        detail = 'Could not validate credentials!' ,
                        headers = {'WWW-Authenticate' : 'Bearer'}
                )
            
            del curr_user['hash_password']
            return curr_user
        except Exception as e :
            print(f'An error occurred {e}')
        except ExpiredSignatureError:
            raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED ,
                    detail = 'Token is expired, please back to log in!' ,
                    headers = {'WWW-Authenticate' : 'Bearer'}
            )
