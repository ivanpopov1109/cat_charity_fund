from typing import Optional
from pydantic import BaseModel, Field, validator, PositiveInt
from datetime import datetime


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt


class DonationDB(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]
    id: int
    create_date: datetime
    invested_amount: Optional[int]
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True


class DonationUser(BaseModel):
    id: int
    comment: Optional[str]
    full_amount: PositiveInt
    create_date: datetime

    class Config:
        orm_mode = True
