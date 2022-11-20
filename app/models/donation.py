from app.core.db import Base
from app.models.basemodel import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey


class Donation(Base, BaseModel):
    comment = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'id: {self.id}, comment: {self.comment}, full_amount: {self.full_amount}'