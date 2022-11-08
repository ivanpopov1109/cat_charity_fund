from app.core.base import Base
from app.models.basemodel import BaseModel
from sqlalchemy import Column, String


class Donation(Base, BaseModel):
    comment = Column(String, nullable=True)

    def __repr__(self):
        return f'id: {self.id}, comment: {self.comment}, full_amount: {self.full_amount}'