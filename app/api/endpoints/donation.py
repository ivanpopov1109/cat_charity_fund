from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.core.db import get_async_session
from app.schemas.donation import DonationCreate, DonationDB
from app.crud.donation import donation_crud
from app.services.invest_new_donate import Invest

router = APIRouter()


@router.post('/', response_model=DonationDB)
async def create_new_donation(donation: DonationCreate,
                              session: AsyncSession = Depends(get_async_session)):
    new_donation = await donation_crud.create(donation, session)
    await Invest.invest(new_donation, session)
    return new_donation


@router.get('/', response_model=list[DonationDB])
async def get_all_donation(session: AsyncSession = Depends(get_async_session)):
    get_all_donation = await donation_crud.get_multi(session)
    return get_all_donation
