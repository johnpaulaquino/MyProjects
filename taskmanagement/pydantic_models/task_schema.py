from pydantic import BaseModel



class UserTask(BaseModel):
    title : str
    description : str