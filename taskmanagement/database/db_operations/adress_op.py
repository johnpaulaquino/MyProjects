from taskmanagement.database.db_engine import create_session
from taskmanagement.database.db_tables.address import Address
from taskmanagement.database.db_tables.users import Users
from sqlalchemy import select, and_


class AddressQueries:
    @staticmethod
    async def add_address(address: Address, user_id : str):
        async with create_session() as session:
            try:
                session.add(address)
                await session.commit()
                await session.refresh(address)
                
                stmt = select(Address).where(and_(Address.user_id == user_id))
                result = await session.execute(stmt)
                user_address = result.scalars().one()
                return user_address.to_dict()
            except Exception as e:
                await session.rollback()
                print(f'An error occurred {e}!')
                return False
