from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends
from app.core.db import get_async_session
from app.schemas.charity_project import CharityProjctCreate, CharityProjectDB
from app.crud.charity_project import charity_project_crud
router = APIRouter()

@router.post('/', response_model=CharityProjectDB)
async def create_new_char_project(charity_project: CharityProjctCreate, session: AsyncSession = Depends(get_async_session)):
    new_char_project = await charity_project_crud.create(charity_project, session)
    return new_char_project