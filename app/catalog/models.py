from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app import Base
from app.auth.models import User


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'user_id': self.user_id,
            'description': self.description,
            'id': self.id,
        }
