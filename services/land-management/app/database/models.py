from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from .database import Base

class Land(Base):
    __tablename__ = "lands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, default='')