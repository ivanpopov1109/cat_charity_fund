from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.schemas.donation import DonationCreate, DonationDB, DonationUser
from app.crud.donation import donation_crud
from app.services.invest_new_donate import invest_new_donate
from app.models import User

router = APIRouter()


@router.post('/', response_model=DonationDB)
async def create_new_donation(donation: DonationCreate,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user)) -> Any:
    new_donation = await donation_crud.create(donation, session, user)
    await invest_new_donate.invest(new_donation, session)
    return new_donation


@router.get('/', response_model=list[DonationDB])
async def get_all_donation(session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_superuser)) -> Any:
    all_donation = await donation_crud.get_multi_by_user(session, user)
    return all_donation


@router.get('/user_donations', response_model=list[DonationUser])
async def get_user_donation(session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_user)) -> Any:
    all_donation_by_user = await donation_crud.get_multi_by_user(session, user)
    return all_donation_by_user
