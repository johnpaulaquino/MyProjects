import asyncio

from taskmanagement.database.db_engine import create_session
from taskmanagement.database.db_tables.task import Tasks
from sqlalchemy import select, and_





class TasksOperations:
    @staticmethod
    async def create_user_tasks(user_task : Tasks):
        async with create_session() as db:
            try:
                db.add(user_task)
                await db.commit()
                await db.refresh(user_task)
                return True
            except Exception as e:
                await db.rollback()
                print(f'An error occurred {e}!')
                return False

print(asyncio.run(TasksOperations.create_user_tasks(
        Tasks(user_id='b63ecb97-edf5-478f-9575-c2108f121a4a',
              description='hhey',
              title='bugok')
)))