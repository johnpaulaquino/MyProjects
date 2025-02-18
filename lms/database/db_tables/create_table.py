from lms.database.db_engine.engine import engine
from lms.database.db_tables.base import Base
from lms.database.db_tables.users import Users
from lms.database.db_tables.address import Address
from lms.database.db_tables.user_additional_info import UserAdditionalInfo
from lms.database.db_tables.book_transactions import BooksTransactions
from lms.database.db_tables.books import Books,EBooks

import asyncio
async def create_table():
    async with engine.begin() as db:
        try:
            await db.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(f'An error occurred {e}!')
            

asyncio.run(create_table())