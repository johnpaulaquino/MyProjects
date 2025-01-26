from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, relationship

from taskmanagement.database.db_tables.base import Base

class Address(Base):
    __tablename__ = 'address'
    
    municipality : str = Column('municipality', String)
    city : str = Column('city', String)
    country : str = Column('country', String)
    postal_code : int = Column('postal_code', Integer)
    user_id : str = Column('user_id', String, ForeignKey('users.id'))
    user : Mapped['Users'] = relationship('Users', back_populates='address', lazy='selectin')
    