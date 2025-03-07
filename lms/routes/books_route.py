from fastapi import APIRouter , Depends, HTTPException, status

from lms.schemas.books_schema import BookSchema
from lms.schemas.paginated_schema import Paginated
from lms.services.books_services import BookServices
from lms.utils.dependencies import Dependencies

books = APIRouter(
        prefix = '/books' ,
        tags = ['Books Services']
)


@books.get('/member/', tags = ['Member'])
async def get_member_books(
        paginated: Paginated = Depends() ,
        curr_user = Depends(Dependencies.get_current_user)) :
    try :
        return await BookServices.get_member_books_services(paginated , curr_user)
    except Exception as e :
        raise e

@books.post('/add',  tags = ['Admin'])
async def add_books(
        book: BookSchema ,
        curr_user = Depends(Dependencies.get_current_user)) :
    try :
            return await BookServices.add_book_services(book , curr_user)
    except Exception as e :
        raise e
