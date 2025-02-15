

from fastapi import APIRouter, Request, HTTPException,Depends, status


from taskmanagement.database.db_operations.tasks_op import TasksOperations
from taskmanagement.pydantic_models.task_schema import UpdateUserTask, UserTask
from taskmanagement.database.db_tables.task import Tasks
from taskmanagement.utils.dependency import Dependencies
from taskmanagement.utils.utility import Utility

task_router = APIRouter(
        prefix='/task',
        tags= ['Task']
)


#Add task
@task_router.post('/create-task')
async def create_user_task(task : UserTask,
                           user_data =  Depends(Dependencies.get_access_token)):
    try:
        
        
        if not user_data:
            raise
        user_task = Tasks(user_id=user_data['user_id'],
                          title=task.title,
                          description=task.description)

        result = await TasksOperations.create_user_tasks(user_task)
        if not result:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Failed to create user task!'
            )
        return {'status' : 'ok',
        'message' : 'success'}
    except Exception as e:
        raise e
    

@task_router.put('/update-task')
async def update_user_task(user_task : UpdateUserTask,
                           user_data = Depends(Dependencies.get_access_token)):
    try:
        
        if not user_data:
            raise
        
        tasks = Tasks(user_id=user_data['user_id'],
                      description=user_task.description,
                      title=user_task.title,
                      status='complete')
        
        await TasksOperations.update_user_task(user_task.task_id, tasks)

        return {'status': 'ok', 'message' : 'Successfully updating user task!'}
    
    except Exception as e:
        print(f'An error occurred {e}!')
        raise e
    
    
@task_router.delete('delete-task')
async def delete_user_task(task_id, user_data = Depends(Dependencies.get_access_token)):
    try:
        if not user_data:
            raise
        
        user_id = user_data['user_id']
        await TasksOperations.delete_user_task(task_id, user_id)
        print('sample')
        return {'status': 'ok',
        'message': 'Successfully deleted task!'}
    except Exception as e:
        print(f'An error occurred {e}!')
        raise e