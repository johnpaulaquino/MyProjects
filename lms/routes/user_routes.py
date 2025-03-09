from fastapi import APIRouter , Depends

from lms.schemas.user_schema import UserUpdateSchema
from lms.services.user_services import UserServices
from lms.utils.dependencies import Dependencies

users_route = APIRouter(
        prefix = '/user/personal-info' ,
        tags = ['User Services']
)


@users_route.put('/update/{user_id}')
async def update_user_personal_info(
        user_id: str ,
        user: UserUpdateSchema ,
        curr_user = Depends(Dependencies.get_current_user)) :
    try :
        return await UserServices.update_personal_info(
            user_id = user_id ,
            user = user ,
            curr_user = curr_user)
    except Exception as e :
        print(f'An error occurred {e}')
        raise e
