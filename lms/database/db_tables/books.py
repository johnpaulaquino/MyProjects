from lms.database.db_tables.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped

from lms.utils.utils import Utility

    
class Books(Base):
    __tablename__ = 'books'
    id: Mapped[int] = Column('id', Integer, primary_key=True, autoincrement=True, unique=True)
    isbn: Mapped[str] = Column('isbn', String, nullable=False)
    author: Mapped[str] = Column('author', String, nullable=False)
    title: Mapped[str] = Column('title', String, nullable=False)
    description: Mapped[str] = Column('description', String)
    copies : Mapped[int] = Column('copies', Integer, nullable=False)
    status : Mapped[str] = Column('status', String, nullable=False)

class EBooks(Base):
    __tablename__ = 'ebooks'
    
    id: Mapped[int] = Column('id', Integer, primary_key=True, autoincrement=True, unique=True)
    isbn: Mapped[str] = Column('isbn', String, nullable=False)
    author: Mapped[str] = Column('author', String, nullable=False)
    title: Mapped[str] = Column('title', String, nullable=False)
    description: Mapped[str] = Column('description', String)
    e_books_url  : Mapped[str] =  Column('e_books_url', String, nullable=False)
    



