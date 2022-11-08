from sqlalchemy import select, func
from app.models.charityproject import CharityProject
from app.models.donation import Donation
from typing import List
from datetime import datetime


class InvestDonate:
    @classmethod
    async def _get_last_char_project(cls, session) -> List[CharityProject]:
        projects = await session.execute(select(CharityProject).where(CharityProject.fully_invested == False).order_by(
            CharityProject.create_date))
        projects = projects.scalars().all()
        return projects

    @classmethod
    def close_obj(cls, obj):
        obj.fully_invested = True
        obj.invested_amount = obj.full_amount
        obj.close_date = datetime.now()

    @classmethod
    async def invest(cls, donate: Donation, session):
        projects = await cls._get_last_char_project(session)
        print(projects)
        for project in projects:
            balance = donate.full_amount - donate.invested_amount
            delta_project = project.full_amount - project.invested_amount
            if balance - delta_project > 0:
                cls.close_obj(project)
                donate.invested_amount += delta_project
                session.add(project, donate)
                continue
            elif balance - delta_project == 0:
                cls.close_obj(project)
                cls.close_obj(donate)
                session.add(donate, project)
                break
            else:
                project.invested_amount += balance
                cls.close_obj(donate)
                session.add(donate, project)
                break

        await session.commit()
        await session.refresh(donate)
        return donate
