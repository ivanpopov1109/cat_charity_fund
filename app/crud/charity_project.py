from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate, CharityProjectDB


class CharityProjectError(Exception):
    pass


class UpdateError(CharityProjectError):
    pass


class CloseProjectError(CharityProjectError):
    """Закрытый объект нельзя удалить или изменить"""
    pass


class AmountError(CharityProjectError):
    """Нельзя установить требуемую сумму меньше уже вложенной"""
    pass


class DelError(CharityProjectError):
    """Нельзя удалить или изменить объект в который уже вложены средства"""
    pass


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_charity_project_id_by_name(charity_project_name: str,
                                             session: AsyncSession) -> int | None:
        charity_project_id = await session.execute(select(CharityProject.id).
                                                   where(CharityProject.name == charity_project_name))
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id

    async def is_exist_name_duplicate(self,
                                      charity_project_name: str,
                                      session: AsyncSession,
                                      ) -> int | None:
        charity_project_id = await self.get_charity_project_id_by_name(charity_project_name, session)
        return charity_project_id

    @staticmethod
    def possible_update_charity_project(new_obj: CharityProjectUpdate,
                                        old_obj: CharityProjectDB) -> None:

        if old_obj.fully_invested:
            raise CloseProjectError
        if old_obj.invested_amount < new_obj.full_amount:
            raise AmountError

    @staticmethod
    def possible_del_charity_project(obj: CharityProject) -> None:
        if obj.invested_amount != 0:
            raise DelError
        if obj.fully_invested:
            raise CloseProjectError


charity_project_crud = CRUDCharityProject(CharityProject)
