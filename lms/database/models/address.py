from lms.database.models.base import Base
from sqlalchemy import Column, String, ForeignKey, Integer

from lms.utils.utils import Utility


class Address(Base):
    __tablename__ = 'address'
    
    id: int = Column('id', Integer, primary_key=True, autoincrement=True, unique=True)
    user_id: str = Column('user_id', String, ForeignKey('users.id'))
    barangay: str = Column('barangay', String, nullable=False)
    municipality: str = Column('municipality', String, nullable=False)
    province: str = Column('province', String, nullable=False)
    country: str = Column('country', String, nullable=False)
    postal_code: str = Column('postal_code', String, nullable=False)
    
    def __init__(
            self, user_id,
            barangay,
            municipality,
            province,
            country,
            postal_code, **kw):
        self.user_id = user_id
        self.barangay = barangay
        self.municipality = municipality
        self.province = province
        self.country = country
        self.postal_code = postal_code
        
        super().__init__(**kw)
    
    def to_dict(self) -> dict:
        return dict(
                id=self.id,
                user_id=self.user_id,
                barangay=self.barangay,
                municipality=self.municipality,
                province=self.province,
                country=self.country,
                postal_code=self.postal_code)
