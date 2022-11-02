from app.core.base import Base
from app.models.basemodel import BaseModel
from sqlalchemy import Column, String

class Donation(Base, BaseModel):
    comment = Column(String, nullable = True )
