from lms.database.db_tables.base import Base
from sqlalchemy import Column, String,Integer

from lms.utils.utils import Utility


class Users(Base):
    __tablename__ = 'users'
    
    id: str = Column('id', String, primary_key=True, default=Utility.generate_uuid)
    firstname: str = Column('firstname', String, nullable=False)
    middle_name: str = Column('middle_name', String, nullable=False)
    lastname: str = Column('lastname', String, nullable=False)
    email: str = Column('email', String, unique=True)
    password: str = Column('password', String, nullable=False)
    status : int = Column('status', Integer,default=0)
    
    
    def __init__(self, firstname,
                 middle_name,
                 lastname,
                 email,
                 password,
                 status = 0,
                 **kw):
        self.firstname = firstname
        self.middle_name = middle_name
        self.lastname = lastname
        self.email = email
        self.password = password
        self.status = status
        super().__init__(**kw)
    
    def to_dict(self) -> dict:
        return dict(
                firstname=self.firstname,
                middle_name=self.middle_name,
                lastname=self.lastname,
                email=self.email,
                password=self.password
        )
