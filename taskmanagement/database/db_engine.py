
from contextlib import asynccontextmanager

#from sql alchemy module
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

#from my projects
from taskmanagement.pydantic_models.settings import Settings
from taskmanagement.database.db_tables.base import Base

#Initialize the settings object
settings = Settings()


URL = settings.DB_URL # This is the URL from the .env file
engine = create_async_engine(URL, echo= True) # To create async engine with the output


#This will create a session to a database
__LocalSession = sessionmaker(
        engine, class_=AsyncSession, autoflush=True, expire_on_commit=False
)

#to create table
async def create_table():
    """
    
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def create_session() -> AsyncSession:
    """
Creates an asynchronous database session using SQLAlchemy.

This function uses a context manager to ensure proper cleanup of the session,
including rollback on errors and closure of the session.

:return:
    An asynchronous SQLAlchemy session.
"""

    async with __LocalSession() as session:
        try:
            yield session # to store the session
        except SQLAlchemyError as e:
            print(f'An error Occurred {e}!')
            await session.rollback()
            
            
            
