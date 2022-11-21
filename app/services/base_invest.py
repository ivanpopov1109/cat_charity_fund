from sqlalchemy import select
from datetime import datetime


class BaseInvest:

    def __init__(self, model_for_invest):
        self._model = model_for_invest

    async def _get_last_open_project(self, session):
        projects = await session.execute(select(self._model).where(self._model.fully_invested == False).order_by(
            self._model.create_date))
        print('from _get_last_open_project:', projects)

        projects = projects.scalars().all()
        print('from _get_last_open_project:', projects)
        return projects

    @classmethod
    def close_obj(cls, obj):
        obj.fully_invested = True
        obj.invested_amount = obj.full_amount
        obj.close_date = datetime.now()

    async def invest(self, donate, session):
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
