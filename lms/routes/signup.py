from fastapi import APIRouter

signup = APIRouter(
        prefix='/create-user',
        tags=['Sign Up']
)


@signup.post('/')
async def create_user_account():
    pass