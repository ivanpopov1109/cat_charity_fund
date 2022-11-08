from sqlalchemy import select
from app.models.charityproject import CharityProject
from app.models.donation import Donation
from typing import List
from datetime import datetime


class Invest:
    @classmethod
    async def _get_last_donation(cls, session) -> List[Donation]:
        projects = await session.execute(select(Donation).where(Donation.fully_invested == False).order_by(
            Donation.create_date))
        projects = projects.scalars().all()
        return projects

    @classmethod
    def close_obj(cls, obj):
        obj.fully_invested = True
        obj.invested_amount = obj.full_amount
        obj.close_date = datetime.now()

    @classmethod
    async def invest(cls, char_project: CharityProject, session):
        donations = await cls._get_last_donation(session)
        for donation in donations:
            balance = char_project.full_amount - char_project.invested_amount
            delta_donation = donation.full_amount - donation.invested_amount
            if balance - delta_donation > 0:
                cls.close_obj(donation)
                char_project.invested_amount += delta_donation
                session.add(donation, char_project)
                continue
            elif balance - delta_donation == 0:
                cls.close_obj(donation)
                cls.close_obj(char_project)
                session.add(donation, char_project)
                break
            else:
                donation.invested_amount += balance
                cls.close_obj(char_project)
                session.add(donation, char_project)
                break

        await session.commit()
        await session.refresh(char_project)
        return char_project
