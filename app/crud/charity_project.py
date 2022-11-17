from app.crud.base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy import select
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(self,
                                             charity_project_name: str,
                                             session: AsyncSession) -> Optional[int]:
        charity_project_id = await session.execute(select(CharityProject.id).
                                                   where(CharityProject.name == charity_project_name))
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id

    async def is_exist_name_duplicate(self,
                                   charity_project_name: str,
                                   session: AsyncSession,
                                   ) -> None:
        charity_project_id = await self.get_charity_project_id_by_name(charity_project_name, session)
        print(charity_project_id)
        return charity_project_id



charity_project_crud = CRUDCharityProject(CharityProject)
