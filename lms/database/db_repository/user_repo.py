
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, and_
from fastapi import HTTPException
from lms.database.db_engine.engine import create_session
from lms.database.models.users import Users

import asyncio

class UserRepository:
    
    @staticmethod
    async def create_user(user : Users ):
        async with create_session() as db:
            try:
                db.add(user)
                await db.commit()
                await db.refresh(user)
                
                return True
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
