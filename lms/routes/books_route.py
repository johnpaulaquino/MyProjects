from fastapi import APIRouter , Depends , HTTPException , status
from starlette.responses import JSONResponse

from lms.schemas.books_schema import BookSchema
from lms.schemas.paginated_schema import Paginated
from lms.services.books_services import BookServices
from lms.utils.dependencies import Dependencies

books = APIRouter(
        prefix = '/books' ,
        tags = ['Books Services']
)


@books.get('/member/' , tags = ['Member'])
async def get_member_books(
        paginated: Paginated = Depends() ,
        curr_user = Depends(Dependencies.get_current_user)) :
    try :
        return await BookServices.get_member_books_services(paginated , curr_user)
    except Exception as e :
        raise e


@books.post('/add-book' , tags = ['Admin'])
async def add_books(
        book: BookSchema ,
        curr_user = Depends(Dependencies.get_current_user)) :
    try :
        return await BookServices.add_book_services(book , curr_user)
    except Exception as e :
        raise e


@books.patch('/update-book/{book_id}' , tags = ['Admin'])
async def update_books(
        book: BookSchema ,
        book_id: int ,
        curr_user = Depends(Dependencies.get_current_user)) :
    try :
        is_updating = await BookServices.update_book_services(
                book = book ,
                book_id = book_id ,
                curr_user = curr_user)
        return is_updating
    except Exception as e :
        raise e


@books.delete('/delete-book/{book_id}', tags = ['Admin'])
async def delete_book(book_id: int , curr_user = Depends(Dependencies.get_current_user)) :
    try :
        return BookServices.delete_book(book_id, curr_user)
    except Exception as e :
        print(f'An error occurred {e}')
        raise e
