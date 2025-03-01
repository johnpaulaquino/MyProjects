
from starlette.responses import JSONResponse

from lms.database.db_repository.book_repo import BooksRepository
from lms.database.models.books import Books
from lms.schemas.books_schema import BookSchema
from lms.schemas.paginated_schema import Paginated
from fastapi import status, HTTPException


class BookServices :
    
    @staticmethod
    async def get_member_books_services(paginated: Paginated , curr_user) :
        try :
            offset = (paginated.skip - 1) * paginated.limit
            books = await BooksRepository.get_books_paginated(offset = offset , limit = paginated.limit)
            if not books :
                return JSONResponse(
                        status_code = status.HTTP_200_OK,
                        content = {'status': 'ok', 'message': 'No books to fetch!'}
                )
            return dict(
                    user = curr_user ,
                    books = books)
        except Exception as e :
            print(f'An error occurred {e}')
            
    @staticmethod
    async def add_book_services(book : BookSchema, curr_user):
        try:
            user_role = curr_user['role']
            
            if user_role == 'member':
                raise HTTPException(
                        status_code = status.HTTP_401_UNAUTHORIZED,
                        detail = 'You are not admin to access this!'
                )
            book_data = Books(
                    isbn = book.isbn,
                    title = book.title,
                    author = book.author,
                    copies = book.copies,
                    status = book.status,
                    description = book.description
            )
            await BooksRepository.add_book(book_data)
            
            return JSONResponse(
                    status_code = status.HTTP_201_CREATED,
                    content = {'status': 'ok', 'message': 'Successfully added book!'}
            )
        except Exception as e:
            print(f'An error occurred {e}')
