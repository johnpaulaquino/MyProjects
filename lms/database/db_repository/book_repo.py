from sqlalchemy import select , update, and_, values, delete
from sqlalchemy.exc import SQLAlchemyError

from lms.database.models.books import Books
from lms.database.db_engine.engine import create_session


class BooksRepository :
    @staticmethod
    async def add_book(book: Books) :
        try :
            async with create_session() as db :
                db.add(book)
                await db.commit()
                await db.refresh(book)
        except Exception as e :
            await db.rollback()
            print(f'An error occurred {e}')
    
    @staticmethod
    async def get_books_paginated(offset: int , limit: int) :
        try :
            async with create_session() as db :
                stmt = select(Books).offset(offset).limit(limit)
                result = await db.execute(stmt)
                books: list = result.scalars().all()
                return books
        except SQLAlchemyError as e :
            print(f'An error occurred {e}')

    @staticmethod
    async def update_book(book : Books, book_id: int):
        try:
            async with create_session() as db:
                stmt = update(Books).where(Books.id == book_id).values(
                        isbn= book.isbn,
                        author= book.author,
                        title = book.title,
                        description = book.description,
                        copies = book.copies,
                        status = book.status)
                
                await db.execute(stmt)
                await db.commit()
                
                stmt1 = select(Books).where(Books.id == book_id)
                result1 = await db.execute(stmt1)
                book1 = result1.scalars().one()
                
                await db.refresh(book1)
                return book1
        except SQLAlchemyError as e:
            await db.rollback()
            print(f'An error occurred {e}')
            return False
    
    @staticmethod
    async def find_book_by_id(book_id):
        try:
            async with create_session() as db:
                stmt = select(Books).where(Books.id == book_id)
                result = await db.execute(stmt)
                book = result.scalars().one()
                
                return book
        except SQLAlchemyError as e:
            print(f'An error occurred {e}')
    
    @staticmethod
    async def delete_book(book_id: int):
        try:
            async with create_session() as db:
                stmt = delete(Books).where(Books.id == book_id)
        except SQLAlchemyError as e:
            print(f'An error occurred {e}')
