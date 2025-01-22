from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import Column, String

from app.utils.utility import Utility

class Base(DeclarativeBase):
    __id : Mapped[str] =  Column('id', String, primary_key=True,
                       unique=True, default=Utility.generate_uuid())
    @property
    def get_id(self):
        return self.__id