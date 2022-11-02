from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.core.db import Base
from app.models.basemodel import BaseModel

class CharityProject(Base, BaseModel):
    name = Column(String(100), unique = True, nullable = False)
    description = Column(Text, nullable = False)

