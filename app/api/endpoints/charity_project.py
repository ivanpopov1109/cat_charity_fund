from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.core.db import get_async_session
from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
from app.crud.charity_project import charity_project_crud
from app.crud.validators import possible_update_charity_project, possible_del_charity_project
from app.services.invest_new_charity import Invest
from app.core.user import current_superuser, current_user
from app.models import User
from fastapi import HTTPException


router = APIRouter()


@router.post('/', response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)])
async def create_new_charity_project(charity_project: CharityProjectCreate,
                                     session: AsyncSession = Depends(get_async_session)):
    if await charity_project_crud.is_exist_name_duplicate(charity_project.name, session):
        raise HTTPException(status_code=404,
                            detail='Объект с таким именем уже существует.')
    new_char_project = await charity_project_crud.create(charity_project, session)
    await Invest.invest(new_char_project, session)
    return new_char_project


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)):
    all_char_projects = await charity_project_crud.get_multi(session)
    return all_char_projects



@router.patch('/{charity_project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)])
async def update_charity_project(charity_project_id: int,
                                 obj_in: CharityProjectUpdate,
                                 session: AsyncSession = Depends(get_async_session),
                                 ):
    charity_project = await charity_project_crud.check_obj_exist(charity_project_id, session)
    if not charity_project:
        raise HTTPException(status_code=404,
                            detail='Объект с таким ID не найден.')
    if obj_in.name is not None:
        name = await charity_project_crud.is_exist_name_duplicate(obj_in.name, session)
        if name:
            raise HTTPException(
                status_code=422,
                detail='Целевой проект с таким именем уже существует.'
            )
    try:
        charity_project_crud.possible_update_charity_project(obj_in, charity_project, session)
    except Exception:
        raise HTTPException(status_code=404,
                            detail='Проект не может быть отредактирован')
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    return charity_project


@router.delete('/{charity_project_id}', response_model=CharityProjectDB, dependencies=[Depends(current_superuser)])
async def del_charity_project(charity_project_id: int,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user)):
    obj = await possible_del_charity_project(charity_project_id, session, user)
    obj = await charity_project_crud.remove(obj, session)
    return obj
