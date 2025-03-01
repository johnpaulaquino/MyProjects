from pydantic import BaseModel



class Paginated(BaseModel):
    skip : int = 1
    limit : int = 10