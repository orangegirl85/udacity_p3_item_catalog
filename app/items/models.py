from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app import Base
from app.auth.models import User
from app.catalog.models import Category


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'id': self.id
        }
