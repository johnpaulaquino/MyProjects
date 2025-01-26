from taskmanagement.database.db_engine import create_table
import asyncio
from taskmanagement.database.db_tables.users import Users
from taskmanagement.database.db_tables.address import Address


#This will create a table
asyncio.run(create_table())


