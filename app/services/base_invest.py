from datetime import datetime
from typing import Generic, TypeVar

from sqlalchemy import select

from app.models.basemodel import BaseModel

Model = TypeVar('Model', bound=BaseModel)


class BaseInvest(Generic[Model]):

    def __init__(self, model_for_invest):
        self._model = model_for_invest

    async def _get_last_open_project(self, session) -> list[Model]:
        projects = await session.execute(select(self._model).where(self._model.fully_invested == False).order_by(
            self._model.create_date))
        projects = projects.scalars().all()
        return projects

    @classmethod
    def close_obj(cls, obj) -> None:
        obj.fully_invested = True
        obj.invested_amount = obj.full_amount
        obj.close_date = datetime.now()

    async def invest(self, donate, session) -> None:
        projects = await self._get_last_open_project(session)
        for project in projects:
            balance = donate.full_amount - donate.invested_amount
            delta_project = project.full_amount - project.invested_amount
            if balance - delta_project > 0:
                self.close_obj(project)
                donate.invested_amount += delta_project
                session.add(project, donate)
                continue
            elif balance - delta_project == 0:
                self.close_obj(project)
                self.close_obj(donate)
                session.add(donate, project)
                break
            else:
                project.invested_amount += balance
                self.close_obj(donate)
                session.add(donate, project)
                break

        await session.commit()
        await session.refresh(donate)
        return donate
