

from taskmanagement.database.db_engine import create_session
from taskmanagement.database.db_tables.task import Tasks
from sqlalchemy import select, and_, update

from taskmanagement.utils.utility import Utility


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
    
    
    @staticmethod
    async def update_user_task(task_id,task : Tasks):
        async with create_session() as db :
            try:
                stmt = update(Tasks).where(and_(Tasks.id == task_id)).values(
                title = task.title, description = task.description, status = task.status
                )
                
                await db.execute(stmt)
                await db.commit()
                
                
                
                return True
            except Exception as e:
                await db.rollback()
                print(f'An error occurred {e}!')
                return False
        



# print(Utility.decode_generated_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBhdWxqb2huLmFwcDIwMjRAZ21haWwuY29tIiwiZXhwIjoxNzM5MTcxMDI3fQ.siMEDTASUsJzpCg1HP6MlSlckA_eII-P6F3bby-AwbQ'))