from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship, Mapped
from datetime import date
from taskmanagement.database.db_tables.base import Base


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
    is_active : bool = Column('is_active', Boolean, default=True)
    age : int = Column('age', Integer,nullable=False)
    b_day : date = Column('b_day', Date, nullable=False)
    address: Mapped['Address'] = relationship('Address',back_populates='user', lazy="selectin")
    
    def __init__(self, email, password, name,age, b_day, **kw):
        self.email = email
        self.name = name
        self.password = password
        self.age = age
        self.b_day = b_day
        super().__init__(**kw)
    
    # # This is a getters methods
    # @property
    # def get_email(self):
    #     return self.email
    #
    # @property
    # def get_password(self):
    #     return self.password
    #
    # @property
    # def get_name(self):
    #     return self.name
    #
    # @property
    # def get_is_active(self):
    #     return self.is_active
    #
    # @property
    # def get_age(self):
    #     return self.age
    #
    # @property
    # def get_b_day(self):
    #     return self.b_day
    #
    # #This is setters methods
    # def set_email(self, email : str):
    #     self.email = email
    #
    # def set_password(self, password : str):
    #     self.password = password
    #
    # def set_name(self, name : str):
    #     self.name = name
    #
    # def set_is_active(self, is_active : bool):
    #     self.is_active = is_active
    #
    # def set_age(self, age):
    #     self.age = age
    #
    # def set_bday(self, b_day : date):
    #     self.b_day = b_day
        
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
    
    