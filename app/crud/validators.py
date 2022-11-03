from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charity_project import charity_project_crud
from app.models.charityproject import CharityProject
from app.schemas.charity_project import CharityProjectUpdate, CharityProjectDB


async def possible_update_charity_project(new_obj: CharityProjectUpdate,
                                          old_obj: CharityProjectDB,
                                          session: AsyncSession) -> None:
    '''
    Закрытый проект нельзя редактировать; нельзя установить требуемую сумму меньше уже вложенной.
    '''
    if old_obj.fully_invested:
        raise HTTPException(detail= 'Закрытый проект нельзя редактировать')
    if old_obj.invested_amount < new_obj.full_amount:
        raise HTTPException(detail= 'Нельзя установить требуемую сумму меньше уже вложенной')



