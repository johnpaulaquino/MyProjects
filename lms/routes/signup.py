from fastapi import APIRouter

print('hey')


signup = APIRouter(
        prefix='/create-user',
        tags=['Sign Up']
)


@signup.post('/')
async def create_user_account():
    pass