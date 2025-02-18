from sqlalchemy.exc import SQLAlchemyError

from lms.database.db_engine.engine import create_session
from lms.database.db_tables.users import Users

import asyncio

class Services:
    @staticmethod
    
    async def create_user(user : Users):
        async with create_session() as session:
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                print('user Created')
            except SQLAlchemyError as e:
                print(f'An error occurred {e}!')
