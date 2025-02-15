from pydantic import BaseModel



class UserTask(BaseModel):
    title : str
    description : str

class UpdateUserTask(UserTask):
    task_id : str