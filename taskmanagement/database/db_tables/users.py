from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship, Mapped
from datetime import date
from taskmanagement.database.db_tables.base import Base
from taskmanagement.database.db_tables.address import Address


"""
    :class
        Users
        
    :table
        users
    :attributes
        email
            should be a unique and this is the data that will use for authentication
        password
            will hashed in the database and this is the data will use for authentication
        name
            is the data that the user will have
        is_active
            is the status of the user account
        age
            is the personal info of user
        b_day
            is the personal info of user
        
"""
class Users(Base):
    
    __tablename__ : str = 'users'
    
    email: str = Column('email', String, unique=True)
    password : str = Column('password', String)
    name : str = Column('name', String, nullable=False)
    is_active : int = Column('is_active', Integer, default=False)
    age : int = Column('age', Integer,nullable=False)
    b_day : date = Column('b_day', Date, nullable=False)

    address: Mapped[list['Address']] = relationship('Address',back_populates='user', lazy="selectin")
    
    def __init__(self, email, password, name,age, b_day, **kw):
        self.email = email
        self.name = name
        self.password = password
        self.age = age
        self.b_day = b_day
        
        super().__init__(**kw)
    
    #This will return the user info as dictionary
    def to_dict(self) -> dict:
        return {
                'id' : self.id,
                'email': self.email,
                'hash_password' : self.password,
                'name': self.name,
                'is_active' : self.is_active,
                'age': self.age,
                'b_day' : self.b_day
        }
    
    