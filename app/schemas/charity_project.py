from typing import  Optional
from pydantic import BaseModel, Field, validators

from datetime import datetime

class CharityProjctCreate(BaseModel):
    name: str
    description: str
    full_amount: int

class CharityProjectDB(BaseModel):
    name: str
    description: str
    full_amount: int
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
    class Config:
        orm_mode = True

class CharityProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]