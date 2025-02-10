from sqlalchemy.orm import Mapped, relationship

from taskmanagement.database.db_tables.base import Base
from sqlalchemy import Column, ForeignKey, String
from taskmanagement.database.db_tables.users import Users


class Tasks(Base):
    __tablename__ = 'tasks'
    
    title: str = Column('title', String, nullable=False)
    description: str = Column('description', String)
    # status contains pending, in-progress and complete
    status: str = Column('status', String, default='pending')
    user_id: str = Column('user_id', String, ForeignKey('users.id'))
    user = relationship('Users', back_populates='task', lazy="selectin")
    
    def __init__(self, title, description, user_id, status = 'pending', **kw):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.status = status
        super().__init__(**kw)
    
    def to_dict(self) -> dict:
        return dict(
                id=self.id,
                user_id=self.user_id,
                title=self.title,
                description=self.description,
                status=self.status,
        )
