
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select , and_ , update
from lms.database.db_engine.engine import create_session
from lms.database.models.users import Users

class UserRepository:
    
    @staticmethod
    async def create_user(user : Users ):
        async with create_session() as db:
            try:
                db.add(user)
                await db.commit()
                await db.refresh(user)
                curr_user = await UserRepository.find_user_by_email(user.email)
                return curr_user
            except SQLAlchemyError as e:
                print(f'An error occurred {e}!')
                await db.rollback()
                return False
    
    @staticmethod
    async def find_user_by_email(email: str) :
        async with create_session() as db :
            try :
                stmt = select(Users).where(and_(Users.email == email))
                result = await db.execute(stmt)
                data = result.scalars().one()
                
                if not data:
                    return False
                
                return data.to_dict()
            except SQLAlchemyError as e :
                print(f'An error occurred {e}')
                return False
            
            
    @staticmethod
    async def activate_user_account(email : str):
        async with create_session() as db :
            try:
                stmt = update(Users).where(and_(Users.email == email)).values(status = 1)
                await db.execute(stmt)
                await db.commit()
                
                
            except SQLAlchemyError as e:
                print(f'An error occurred {e}')
                await db.rollback()
    
    @staticmethod
    async def find_user_by_user_id(user_id: str) :
        async with create_session() as db :
            try :
                stmt = select(Users).where(and_(Users.id == user_id))
                result = await db.execute(stmt)
                data = result.scalars().one()
                
                if not data :
                    return False
                
                return data.to_dict()
            except SQLAlchemyError as e :
                print(f'An error occurred {e}')
                return False