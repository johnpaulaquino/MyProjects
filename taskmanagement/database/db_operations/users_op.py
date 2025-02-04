import asyncio

from taskmanagement.database.db_engine import create_session
from taskmanagement.database.db_tables.address import Address
from taskmanagement.database.db_tables.users import Users

from sqlalchemy import select, and_, update
from sqlalchemy.exc import SQLAlchemyError


class UsersQueries:
    
    @staticmethod
    async def create_user(user : Users):
        """
        This will create a user and save into database
        :param user:
            is an instance of object to create and save in database
        :return:
            True if added successfully, otherwise return False
        """
        async with create_session() as db:
            try:
                db.add(user)
                await db.commit()
                await db.refresh(user)
                return user.to_dict()
            except SQLAlchemyError as e:
                print(f'An error occurred {e}!')
                await db.rollback()
                return False
    
    @staticmethod
    async def create_user_address(address : Address):
        async with create_session() as db:
            try:
                db.add(address)
                await db.commit()
                await db.refresh(address)
                return True
            except SQLAlchemyError as e:
                await db.rollback()
                print(f'An error occurred {e}!')
                return False
    
    @staticmethod
    async def find_user_by_email(email : str):
        """
        This will be to search data in the database by a Email, because email is unique.
        :param email:
            is one of unique identifier in user information.
        :return:
            return the info of the users in a dictionary.
        """
        async with create_session() as db:
            try:
                stmt = (select(Users).
                        where(and_(Users.email == email)))
                result = await db.execute(stmt)
                user_result = result.scalars().one()
                return user_result.to_dict()
            except SQLAlchemyError as e:
                print(f'An error occurred {e}')
                return False
    
    @staticmethod
    async def activate_user(email: str ):
        
        async with create_session() as db:
            try:
                stmt = update(Users).where(and_(Users.email == email))
                await db.execute(stmt)
                await db.commit()
                
                stmt1 = select(Users).where(and_(Users.email == email))
                result = await db.execute(stmt1)
                user = result.scalars().one()
                
                if not user:
                    return False
                
                await db.refresh(user)
                return True
            except SQLAlchemyError as e:
                await db.rollback()
                
                print(f'An error occurred {e}!')
                return False