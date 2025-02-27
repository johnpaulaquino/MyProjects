from fastapi import APIRouter




library = APIRouter(
        prefix = '/books',
        tags = ['Books']
)