from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends
from app.core.db import get_async_session
from app.schemas.charity_project import CharityProjctCreate, CharityProjectDB, CharityProjectUpdate
from app.crud.charity_project import charity_project_crud
from app.crud.validators import possible_update_charity_project

router = APIRouter()


@router.post('/', response_model=CharityProjectDB)
async def create_new_charity_project(charity_project: CharityProjctCreate,
                                     session: AsyncSession = Depends(get_async_session)):
    new_char_project = await charity_project_crud.create(charity_project, session)
    return new_char_project


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)):
    all_char_projects = await charity_project_crud.get_multi(session)
    return all_char_projects


@router.patch('/{charity_project_id}',
              response_model=CharityProjectDB)
async def update_charity_project(charity_project_id: int,
                                 obj_in: CharityProjectUpdate,
                                 session: AsyncSession = Depends(get_async_session)):
    charity_project = await charity_project_crud.check_obj_exist(charity_project_id, session)
    if obj_in.name is not None:
        await charity_project_crud.check_name_duplicate(obj_in.name, session)

    possible_update_charity_project(obj_in,charity_project, session)
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    return charity_project




