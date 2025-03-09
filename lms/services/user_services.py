from fastapi import HTTPException, status
from starlette.responses import JSONResponse

from lms.database.db_repository.user_repo import UserRepository
from lms.database.models.users import Users
from lms.schemas.user_schema import UserUpdateSchema


class UserServices:
    
    
    @staticmethod
    async def update_personal_info(user : UserUpdateSchema, user_id : str, curr_user):
        try:
            curr_user_id = curr_user['id']
            
            user_update = Users(
                    firstname =  user.firstname,
                    middle_name = user.middle_name,
                    lastname = user.lastname,
                    email = None,
                    password = None)
            if curr_user_id != user_id:
                raise HTTPException(
                        status_code = status.HTTP_401_UNAUTHORIZED,
                        detail = "You don't have rights to update others information!"
                )
            
            if not await UserRepository.find_user_by_user_id(user_id):
                raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        detail = 'User is not exist'
                )
            
            await UserRepository.update_personal_info(user_id, user_update)
            return JSONResponse(
                    status_code = status.HTTP_200_OK,
                    content = {'message' : 'Successfully update your information'}
            )
        except Exception as e:
            print(f'An error occurred {e}')
            raise e