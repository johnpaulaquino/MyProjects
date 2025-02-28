from lms.database.models.base import Base
from sqlalchemy import Column , String , Integer
from sqlalchemy.orm import Mapped


class Books(Base) :
    __tablename__ = 'books'
    id: Mapped[int] = Column('id' , Integer , primary_key = True , autoincrement = True , unique = True)
    isbn: Mapped[str] = Column('isbn' , String , nullable = False)
    author: Mapped[str] = Column('author' , String , nullable = False)
    title: Mapped[str] = Column('title' , String , nullable = False)
    description: Mapped[str] = Column('description' , String)
    copies: Mapped[int] = Column('copies' , Integer , nullable = False)
    status: Mapped[str] = Column('status' , String , nullable = False)
    # e_books_url: Mapped[str] = Column('e_books_url' , String , nullable = False)

    def __init__(self , isbn , author , title , description , copies , status , **kw) :
        self.isbn = isbn
        self.author = author
        self.title = title
        self.description = description
        self.copies = copies
        self.status = status
        
        super().__init__(**kw)


class EBooks(Base) :
    __tablename__ = 'ebooks'
    
    id: Mapped[int] = Column('id' , Integer , primary_key = True , autoincrement = True , unique = True)
    isbn: Mapped[str] = Column('isbn' , String , nullable = False)
    author: Mapped[str] = Column('author' , String , nullable = False)
    title: Mapped[str] = Column('title' , String , nullable = False)
    description: Mapped[str] = Column('description' , String)
    e_books_url: Mapped[str] = Column('e_books_url' , String , nullable = False)
    
    def __init__(self , isbn , author , title , description , e_books_url, **kw) :
        self.isbn = isbn
        self.author = author
        self.title = title
        self.description = description
        self.e_books_url = e_books_url
        
        super().__init__(**kw)