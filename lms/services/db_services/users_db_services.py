from sqlalchemy.exc import SQLAlchemyError

from lms.database.db_repository.user_repo import UserRepository
from fastapi import BackgroundTasks , HTTPException , status , Response

from lms.database.models.users import Users
from lms.utils.utils import Utility


class UserDbServices :
    @staticmethod
    async def create_user(user_cred , background_task: BackgroundTasks) :
        try :
            # query the email if exists in the db or not
            is_email_find = await UserRepository.find_user_by_email(user_cred.email)
            
            # check whether the email is in db nad if in db will check if it is active or not.
            if is_email_find :
                # if it is active then will raise an error
                if is_email_find['status'] :
                    raise HTTPException(
                            status_code = status.HTTP_400_BAD_REQUEST ,
                            detail = 'Email is already exist!'
                    )
                # otherwise, it will set the status code to 200 and return a response message
                return {'status'  : 'ok' ,
                        'message' : 'it seems you have an account,'
                                    'but need to verify'}
            
            # otherwise, it will create a new user
            user = Users(
                    firstname = user_cred.firstname ,
                    middle_name = user_cred.middle_name ,
                    lastname = user_cred.lastname ,
                    email = user_cred.email ,
                    password = Utility.hash_plain_password(user_cred.password)
            )
            new_user = await UserRepository.create_user(user)
            
            if not new_user :
                raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST ,
                        detail = 'Failed to create user!'
                )
            
            
            code = Utility.generate_verification_code()
            # This will send the task in a background. the param sequence
            # should be, function, email, message and subject
            email_message = f'Use this code to verify your account {code}.'
            background_task.add_task(Utility.send_email , user.email , email_message , 'verification code')
            return {'status'  : 'ok' ,
                    'message' : 'Please check your email for verification code!'}
        except SQLAlchemyError as e :
            print(f'An error occurred {e}')
