from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import Column, String

from taskmanagement.utils.utility import Utility

class Base(DeclarativeBase):
    __abstract__ = True
    
    id : Mapped[str] =  Column('id', String, primary_key=True,
                       unique=True, default=Utility.generate_uuid())
