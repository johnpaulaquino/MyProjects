from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.suite.test_reflection import users

from app.database.db_tables.base import Base



class Users(Base):
    __tablename__ : str = 'users'
    
    __email: str = Column('email', String, unique=True)
    __password : str = Column('password', String)
    __name : str = Column('name', String)
    __is_active : bool = Column('is_active', Boolean, default=True)
    
    
    def __init__(self, email, password, name, **kw):
        self.__email = email
        self.__name = name
        self.__password = password
        super().__init__(**kw)
    
    # This is a getters methods
    @property
    def get_email(self):
        return self.__email
    
    @property
    def get_password(self):
        return self.__password
    
    @property
    def get_name(self):
        return self.__name
    
    @property
    def get_is_active(self):
        return self.__is_active
    
    #This is setters methods
    
  
    def set_email(self, email : str):
        self.__email = email
    
    
users1 = Users(email='as',password='asd',name='as')