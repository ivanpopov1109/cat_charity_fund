from sqlalchemy import Column, String, Text
from app.core.db import Base
from app.models.basemodel import BaseModel

class CharityProject(Base, BaseModel):
    name = Column(String(100), unique = True, nullable = False)
    description = Column(Text, nullable = False)

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}, desc: {self.description}, date_create: {self.create_date}, date_close: {self.close_date}'

