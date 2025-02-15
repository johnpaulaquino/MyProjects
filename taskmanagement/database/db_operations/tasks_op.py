

from taskmanagement.database.db_engine import create_session
from taskmanagement.database.db_tables.task import Tasks
from sqlalchemy import delete, select, and_, update
from fastapi import HTTPException, status
from taskmanagement.utils.utility import Utility


class TasksOperations:
    @staticmethod
    async def create_user_tasks(user_task: Tasks):
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
    async def update_user_task(task_id, task: Tasks):
        async with create_session() as db:
            try:
                is_user_task_exist = await TasksOperations.get_user_task_by_id(task_id)
                if not is_user_task_exist:
                    raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail='The task you are trying to update is not exist!'
                    )
                
                if task.user_id != is_user_task_exist['user_id']:
                    raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You don't have rights to update this!"
                    )
                stmt = update(Tasks).where(and_(Tasks.id == task_id)
                                           ).values(
                        title=task.title,
                        description=task.description,
                        status=task.status
                )
                await db.execute(stmt)
                await db.commit()
                
                return True
            except Exception as e:
                await db.rollback()
                print(f'An error occurred {e}!')
                raise e
            
            
    @staticmethod
    async def delete_user_task(task_id, user_id):
        async with create_session() as db:
            try:
                is_user_task_exist = await TasksOperations.get_user_task_by_id(task_id)
                if not is_user_task_exist:
                    raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail='The task you are trying to delete is not exist!'
                    )
                
                if user_id != is_user_task_exist['user_id']:
                    raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You don't have rights to delete this!"
                    )
                stmt = delete(Tasks).where(
                    and_(Tasks.id == task_id))
                await db.execute(stmt)
                await db.commit()
                
                return True
            except Exception as e:
                await db.rollback()
                print(f'An error occurred {e}!')
                raise e
            
    @staticmethod
    async def get_user_task_by_id(task_id : str):
        try:
            async with create_session() as session :
                stmt = select(Tasks).where(and_(Tasks.id == task_id))
                result = await session.execute(stmt)
                user_task = result.scalars().one()
                
                if not user_task:
                    return False
                
                return user_task.to_dict()
        except Exception as e:
            print(f'An error occurred {e}!')
            return False

# print(Utility.decode_generated_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBhdWxqb2huLmFwcDIwMjRAZ21haWwuY29tIiwiZXhwIjoxNzM5MTcxMDI3fQ.siMEDTASUsJzpCg1HP6MlSlckA_eII-P6F3bby-AwbQ'))
