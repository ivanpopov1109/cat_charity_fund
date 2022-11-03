from app.crud.base import CRUDBase
from app.models.charityproject import CharityProject
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import Optional
from sqlalchemy import select
from app.models.charityproject import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(self,
                                             charity_project_name: str,
                                             session: AsyncSession) -> Optional[int]:
        charity_project_id = await session.execute(select(CharityProject.id).
                                                   where(CharityProject.name == charity_project_name))
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id

    async def check_name_duplicate(self,
                                   charity_project_name: str,
                                   session: AsyncSession,
                                   ) -> None:
        charity_project_id = await self.get_charity_project_id_by_name(charity_project_name, session)
        if charity_project_id is not None:
            raise HTTPException(
                status_code=422,
                detail='Целевой проект с таким именем уже существует!',
            )



charity_project_crud = CRUDCharityProject(CharityProject)
