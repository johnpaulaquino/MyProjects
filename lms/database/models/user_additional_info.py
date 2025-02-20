from datetime import datetime, date
from lms.database.models.base import Base
from sqlalchemy import Column, String, Integer, Date, ForeignKey


class UserAdditionalInfo(Base):
    __tablename__ = 'add_info'


    id : int = Column('id', Integer, primary_key=True, autoincrement=True, unique=True)
    user_id : str = Column('user_id', String, ForeignKey('users.id'))
    profile_url : str = Column('profile_url', String)
    username : str = Column('username', String)
    birth_date : date = Column('birth_date', Date, nullable=False)
    age : int = Column('age', Integer, nullable=False)
    
    
