from app.crud.base import CRUDBase
from app.models.donation import Donation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User


class CRUDDonation(CRUDBase):
    async def get_multi(
            self,
            session: AsyncSession,
            user: User
    ):
        print(user.is_superuser)
        db_objs = await session.execute(
            select(self.model).where(self.model.user_id == user.id)) if not user.is_superuser else await session.execute(
            select(self.model))
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
