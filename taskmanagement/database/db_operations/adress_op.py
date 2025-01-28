from taskmanagement.database.db_engine import create_session
from taskmanagement.database.db_tables.address import Address
from taskmanagement.database.db_tables.users import Users
from sqlalchemy import select


class AddressQueries:
    @staticmethod
    async def add_address(address: Address):
        async with create_session() as session:
            try:
                session.add(address)
                await session.commit()
                await session.refresh(address)
                return True
            except Exception as e:
                await session.rollback()
                print(f'An error occurred {e}!')
                return False
    
    @staticmethod
    async def get_address_by_id():
        async with create_session() as session:
            try:
                stmt = (select(
                        Users.id, Users.name, Users.email, Users.age, Users.b_day,
                        Address.id, Address.municipality, Address.city, Address.country, Address.postal_code)
                        .join(Address, Users.id == Address.user_id))
                result = await session.execute(stmt)
                users_full_info = result.scalars().one()
                return users_full_info
            except Exception as e:
                print(f'An error occurred {e}!')
                return False
