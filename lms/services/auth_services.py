from sqlalchemy.exc import SQLAlchemyError

from lms.database.db_repository.user_repo import UserRepository
from fastapi import BackgroundTasks , HTTPException , status
from lms.database.models.users import Users
from lms.services.email_services import EmailServices
from lms.services.users_cache_services import UsersCacheServices
from lms.services.verification_code_cache import VerificationCache
from lms.utils.generator_utils import GeneratorUtils
from lms.utils.auth_utils import AuthUtility


generator_utils = GeneratorUtils()

class AuthServices :
    @staticmethod
    async def create_user_account(user_cred , background_task: BackgroundTasks) :
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
            
          
           
            
            code = generator_utils.generate_verification_code()
            # This will send the task in a background. the param sequence
            # should be, function, email, message and subject
            email_message = f'Use this code to verify your account {code}.'
            
            # otherwise, it will create a new user
            user = Users(
                    firstname = user_cred.firstname ,
                    middle_name = user_cred.middle_name ,
                    lastname = user_cred.lastname ,
                    email = user_cred.email ,
                    password = AuthUtility.hash_plain_password(user_cred.password)
            )
            
            new_user = await UserRepository.create_user(user)
            
            if not new_user :
                raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST ,
                        detail = 'Failed to create user!'
                )
            background_task.add_task(EmailServices.email_message , email_message, user.email , 'verification code')
            await VerificationCache.store_otp(user.email, code, generator_utils.get_interval())
            await UsersCacheServices.insert_user_cred(new_user['id'], new_user)
            return {'status'  : 'ok' ,
                    'message' : 'Please check your email for verification code!'}
        except SQLAlchemyError as e :
            print(f'An error occurred {e}')
            
    
    @staticmethod
    async def verify_user_account(email : str, code : str):
        try:
            is_code_expired = await VerificationCache.retrieve_otp(email)
            # check if the email is not none
            if not email:
                raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        detail = 'Email must be filled'
                )
            
            #check if the verification code is expired or not
            if not is_code_expired:
                raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST ,
                        detail = 'Verification is expired!'
                )
            
            #will check the code if it is correct
            if not generator_utils.verify_code_verification(code):
                raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        detail = 'Wrong verification code, please try again!'
                )
            await UserRepository.activate_user_account(email)# update the user data in the db
            await VerificationCache.delete_otp(email) #Delete the verification code in the redis
            return {'status': 'ok', 'message': 'activated!, please proceed to log in!'}
        except Exception as e:
            print(f'An error occurred {e}')
            raise e
        
        
    @staticmethod
    async def re_send_code(email : str, background_task : BackgroundTasks):
        try:
            is_code_expired = await VerificationCache.retrieve_otp(email)
            if not email :
                raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        detail = 'Email must be filled'
                )
            if is_code_expired:
                raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        detail = "You cannot re-send, because OTP is not expired, "
                                 "please check your email!"
                )
            code = generator_utils.generate_verification_code()
            # This will send the task in a background. the param sequence
            # should be, function, email, message and subject
            email_message = f'Use this code to verify your account {code}.'
            background_task.add_task(EmailServices.email_message , email_message , email , 'Verification code')
            await VerificationCache.store_otp(email , code , generator_utils.get_interval())
        except Exception as e:
            print(f'An error occurred {e}')
            raise e