from sqlalchemy import Column, Integer, String
from app import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(250))
    email = Column(String(250), nullable=False)
