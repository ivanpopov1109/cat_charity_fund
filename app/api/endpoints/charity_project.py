from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.core.db import get_async_session
from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
from app.crud.charity_project import charity_project_crud, CloseProjectError, DelError, AmountError
from app.services.invest_new_charity import invest_new_charity
from app.core.user import current_superuser
from fastapi import HTTPException
from http import HTTPStatus

router = APIRouter()


@router.post('/', response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)])
async def create_new_charity_project(charity_project: CharityProjectCreate,
                                     session: AsyncSession = Depends(get_async_session)):
    if await charity_project_crud.is_exist_name_duplicate(charity_project.name, session):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Объект с таким именем уже существует.')
    new_char_project = await charity_project_crud.create(charity_project, session)
    await invest_new_charity.invest(new_char_project, session)
    return new_char_project


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)) -> list[CharityProjectDB]:
    all_char_projects = await charity_project_crud.get_multi(session)
    return all_char_projects


@router.patch('/{charity_project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)])
async def update_charity_project(charity_project_id: int,
                                 obj_in: CharityProjectUpdate,
                                 session: AsyncSession = Depends(get_async_session),
                                 ) -> CharityProjectDB:
    charity_project = await charity_project_crud.check_obj_exist(charity_project_id, session)
    if not charity_project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Объект с таким ID не найден.')
    if obj_in.name is not None:
        name = await charity_project_crud.is_exist_name_duplicate(obj_in.name, session)
        if name:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Целевой проект с таким именем уже существует.'
            )
    try:
        charity_project_crud.possible_update_charity_project(obj_in, charity_project, session)
    except CloseProjectError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Закрытый проект нельзя изменить.')
    except AmountError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Нельзя установить требуемую сумму меньше уже внесенной.')
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    return charity_project


@router.delete('/{charity_project_id}', response_model=CharityProjectDB, dependencies=[Depends(current_superuser)])
async def del_charity_project(charity_project_id: int,
                              session: AsyncSession = Depends(get_async_session)):
    obj = await charity_project_crud.check_obj_exist(charity_project_id, session)
    if not obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Объект с таким id не найден')
    try:
        charity_project_crud.possible_del_charity_project(obj)
    except DelError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Нельзя удалить объект в который в который уже были внесены средства.')
    except CloseProjectError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Закрытый проект нельзя удалить')

    obj = await charity_project_crud.remove(obj, session)
    return obj

