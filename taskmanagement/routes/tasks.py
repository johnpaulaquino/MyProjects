from fastapi import APIRouter, Request
from fastapi.params import Depends

from taskmanagement.database.db_operations.tasks_op import TasksOperations
from taskmanagement.pydantic_models.task_schema import UserTask
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
                           user_data : dict =  Depends(Dependencies.get_access_token)):
    
    try:
        
        user_task = Tasks(user_id=user_data['id'],
                          title=task.title,
                          description=task.description)
        result = TasksOperations.create_user_tasks(user_task)
        return {'user_task' : result}
    except Exception as e:
        print(f'An error occurred {e}!')
