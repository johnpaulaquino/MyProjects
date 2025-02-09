from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Request

from taskmanagement.utils.utility import Utility

activity = {}


class Dependencies:
    @staticmethod
    def inactive_tracker(request: Request, token: str):
        def dependency():
            limit_of_inactive = timedelta(minutes=30)
            current_act = datetime.now(timezone.utc)
            try:
                user_cred = Utility.decode_generated_token(token)
            except Exception as e:
                raise e
            
            user_id = user_cred['id']
            if user_id in activity:
                time_now = datetime.now(timezone.utc)
                if (time_now - activity[current_act]) > limit_of_inactive:
                    
                    raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Your session has been expired'
                    )
                
                activity[user_id] = current_act
        
        return dependency
    
    @staticmethod
    def get_access_token(request: Request):
        access_token = request.cookies.get('access_token')
        if not access_token:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Missing auth token, please login again!')
        try:
            payload = Utility.decode_generated_token(access_token)
            if not payload:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Invalid credentials!',
                        headers={'WWW-Authenticate': 'Bearer'}
                )
            return payload
        except Exception as e:
            print(f'An error occurred {e}!')
