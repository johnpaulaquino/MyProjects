from app.database.db_engine import create_table
import asyncio
from app.database.db_tables.users import Users



asyncio.run(create_table())


