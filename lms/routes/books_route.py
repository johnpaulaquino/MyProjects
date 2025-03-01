from fastapi import APIRouter , Depends

from lms.schemas.books_schema import BookSchema
from lms.schemas.paginated_schema import Paginated
from lms.services.books_services import BookServices
from lms.utils.dependencies import Dependencies

books = APIRouter(
        prefix = '/books' ,
        tags = ['Books']
)


@books.get('/member/')
async def get_member_books(
        paginated: Paginated = Depends() ,
        curr_user = Depends(Dependencies.get_current_user)) :
    try :
        return await BookServices.get_member_books_services(paginated , curr_user)
    except Exception as e :
        print(f'An error occurred {e}')
        raise e


@books.get('/total-number')
async def get_total_of_books() :
    try :
        pass
    except Exception as e :
        print(f'An error occurred {e}')


@books.post('/add')
async def add_books(
        book: BookSchema ,
        curr_user = Depends(Dependencies.get_current_user)) :
    try :
        return await BookServices.add_book_services(book, curr_user)
    except Exception as e :
        print(f'An error occurred {e}')
        raise e
