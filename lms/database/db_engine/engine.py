from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from lms.schema_models.settings import Settings



settings = Settings()

'''
@:var engine
    - This engine contains the url for database, to make a connection in db
'''
engine = create_async_engine(
        settings.DB_URL,
        echo= True
)
# Create a session factory
localSession = sessionmaker(class_=AsyncSession,bind= engine,
                            autoflush=False,
                            expire_on_commit = False)

@asynccontextmanager
async def create_session() -> AsyncSession:
    """
           Asynchronous context manager for managing database sessions.

           This function provides a safe way to manage database sessions in an asynchronous application. It ensures that
           sessions are properly created, errors are handled, and sessions are closed after use.

           Yields:
               AsyncSession: An instance of the database session to perform database operations.

           Raises:
               SQLAlchemyError: If a database-related error occurs, it is logged and re-raised for further handling.
           """
    async with localSession() as session:
        try:
            yield session
        except Exception as e:
            print(f'An error occurred {e}!')
            session.rollback()
            
            
        

