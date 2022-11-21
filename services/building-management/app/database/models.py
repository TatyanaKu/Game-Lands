from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from .database import Base

class Building(Base):
    __tablename__ = "building"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, default='')
    level = Column(Integer)
    type = Column(String)
    landid = Column(Integer)