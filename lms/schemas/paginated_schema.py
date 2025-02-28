from pydantic import BaseModel



class Paginated(BaseModel):
    skip : int = 0
    limit : int = 10