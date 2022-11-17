from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.charity_project import CharityProjectUpdate, CharityProjectDB
from app.crud.charity_project import charity_project_crud
from app.models.charityproject import CharityProject
from app.models import User





async def possible_update_charity_project(new_obj: CharityProjectUpdate,
                                          old_obj: CharityProjectDB,
                                          user: User) -> None:
    '''
    Закрытый проект нельзя редактировать; нельзя установить требуемую сумму меньше уже вложенной.
    '''
    if old_obj.fully_invested:
        raise HTTPException(detail='Закрытый проект нельзя редактировать')
    if old_obj.invested_amount < new_obj.full_amount:
        raise HTTPException(detail='Нельзя установить требуемую сумму меньше уже вложенной')
    if not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='У пользователя нет прав на удаление'
        )


async def possible_del_charity_project(obj_id: int,
                                       session: AsyncSession,
                                       user: User) -> CharityProject:
    obj = await charity_project_crud.check_obj_exist(obj_id, session)
    if not obj:
        raise HTTPException(status_code=404,
                            detail='Объект с таким ID не найден!')
    if obj.invested_amount != 0:
        raise HTTPException(status_code= 404, detail='Нельзя удалить проект в который уже были инвестированы средства,'
                                   'его можно только закрыть.')
    if not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='У пользователя нет прав на удаление'
        )
    return obj
