from fastapi import APIRouter

from taskmanagement.database.db_operations.adress_op import AddressQueries
from taskmanagement.pydantic_models.address_model import AddressBase
from taskmanagement.database.db_tables.address import Address

user_address = APIRouter(
        prefix='/add-address',
        tags=['Signup']
)


@user_address.post('')
async def create_user_address(address: AddressBase):
    try:
        address_user = Address(
                address.country
        )
        result= AddressQueries.add_address()
    
    except Exception as e:
        print(f'An error occurred {e}!')
    pass
    