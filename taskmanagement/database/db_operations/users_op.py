import asyncio

from taskmanagement.database.db_engine import create_session
from taskmanagement.database.db_tables.users import Users

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError


class UsersQueries:
    
    @staticmethod
    async def create_user(user : Users):
        async with create_session() as db:
            try:
                if await UsersQueries.find_user_by_email(user.email):
                    return False
                db.add(user)
                await db.commit()
                await db.refresh(user)
                return True
            except SQLAlchemyError as e:
                print(f'An error occurred {e}!')
                await db.rollback()
                return False
    
    @staticmethod
    async def find_user_by_email(email : str):
        async with create_session() as db:
            try:
                stmt = (select(Users).
                        where(Users.email == email))
                result = await db.execute(stmt)
                user_result = result.scalars().one()
                return user_result.to_dict()
            except SQLAlchemyError as e:
                print(f'An error occurred {e}')
                return False

# print(asyncio.run(UsersQueries.find_user_by_email('paul@gmail.com')))
