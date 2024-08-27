from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    created_at = Column(DateTime)
    tweets = relationship("Tweet", back_populates="user")
