from lms.database.models.base import Base

from sqlalchemy import Column, String, Date,ForeignKey, Integer
from datetime import date
from lms.utils.utils import Utility


class BooksTransactions(Base):
    __tablename__ = 'book_transactions'
    
    
    id : int = Column('id', Integer, primary_key=True, autoincrement=True, unique=True)
    user_id : str = Column('user_id', String, ForeignKey('users.id'))
    book_id : int = Column('book_id', Integer, ForeignKey('books.id'))
    borrow_date  : date = Column('borrow_date', Date, nullable=False)
    return_date : date = Column('return_date', Date, nullable=False)