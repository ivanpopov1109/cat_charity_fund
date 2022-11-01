from app.core.base import Base
from app.models.BaseModel import BaseModel
from sqlalchemy import Column, String

class Donation(Base, BaseModel):
    comment = Column(String, nullable = True )
