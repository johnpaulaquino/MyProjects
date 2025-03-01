from pydantic import BaseModel


class BookSchema(BaseModel):
    isbn : str
    author : str
    title : str
    description : str
    copies : int
    status : str