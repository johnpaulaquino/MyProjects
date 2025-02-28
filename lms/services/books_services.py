from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from lms.database.models.books import Books
from lms.database.db_engine.engine import create_session



class BooksServices:
    @staticmethod
    async def add_book(book : Books):
        try:
            async with create_session() as db:
                db.add(book)
                await db.commit()
                await db.refresh(book)
        except Exception as e:
            await db.rollback()
            print(f'An error occurred {e}')
    
    
    @staticmethod
    async def get_books_paginated(offset: int, limit: int):
        try:
            async with create_session() as db:
                stmt = select(Books).offset(offset).limit(limit)
                result = await db.execute(stmt)
                books : list = result.scalars().all()
                return books
        except SQLAlchemyError as e:
            print(f'An error occurred {e}')
            
    
    