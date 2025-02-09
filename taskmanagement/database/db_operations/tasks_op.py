from taskmanagement.database.db_engine import create_session
from taskmanagement.database.db_tables.task import Tasks
from sqlalchemy import select, and_





class TasksOperations:
    @staticmethod
    async def create_user_tasks(task : Tasks):
        async with create_session() as session:
            try:
                await session.add(task)
                await session.commit()
                await session.refresh(task)
                
                stmt = select(Tasks).where(and_(Tasks.user_id == task.user_id))
                result = await session.execute(stmt)
                user_tasks = result.scalars().all()
                
                if not user_tasks:
                    return False
                
                return user_tasks
            except Exception as e:
                await session.rolback()
                print(f'An error occurred {e}!')

