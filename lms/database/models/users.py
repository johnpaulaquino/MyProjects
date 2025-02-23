from lms.database.models.base import Base
from sqlalchemy import Column , String , Integer , TIMESTAMP , func
from lms.utils.generator_utils import GeneratorUtils


class Users(Base) :
    __tablename__ = 'users'
    
    id: str = Column('id' , String , primary_key = True , default = GeneratorUtils.generate_uuid)
    firstname: str = Column('firstname' , String , nullable = False)
    middle_name: str = Column('middle_name' , String , nullable = False)
    lastname: str = Column('lastname' , String , nullable = False)
    email: str = Column('email' , String , unique = True)
    password: str = Column('password' , String , nullable = False)
    status: int = Column('status' , Integer , default = 0)
    created_at = Column('created_at' , TIMESTAMP , server_default = func.now())
    
    def __init__(
            self , firstname ,
            middle_name ,
            lastname ,
            email ,
            password ,
            status = 0 ,
            **kw) :
        self.firstname = firstname
        self.middle_name = middle_name
        self.lastname = lastname
        self.email = email
        self.password = password
        self.status = status
        super().__init__(**kw)
    
    def to_dict(self) -> dict :
        return dict(
                id = self.id ,
                firstname = self.firstname ,
                middle_name = self.middle_name ,
                lastname = self.lastname ,
                email = self.email ,
                hash_password = self.password ,
                status = self.status
        )
