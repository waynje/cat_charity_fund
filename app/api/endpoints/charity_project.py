from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_name_duplicate, check_project_exists, 
    check_project_closed, check_correct_amount_to_update, 
    check_project_was_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

router = APIRouter()


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):

    projects = await charityproject_crud.get_multiple(session)
    return projects


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):

    await check_project_name_duplicate(charity_project.name,
                                       session)
    new_project = await charityproject_crud.create(charity_project,
                                                   session)
    # создание сбора через функцию
    await session.refresh(new_project)
    return new_project


@router.patch('/{project_id}',
              dependencies=[Depends(current_superuser)],
              response_model=CharityProjectDB)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):

    current_project = await check_project_exists(project_id,
                                                 session)
    await check_project_closed(project_id,
                               session)

    if obj_in.full_amount is not None:
        await check_correct_amount_to_update(project_id,
                                             session,
                                             obj_in.full_amount)

    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name,
                                           session)

    current_project = await charityproject_crud.update(current_project,
                                                       obj_in,
                                                       session)
    return current_project


@router.delete('/{project_id}',
               dependencies=[Depends(current_superuser)])
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):

    current_project = await check_project_exists(project_id,
                                                 session)
    await check_project_was_invested(project_id,
                                     session)
    current_project = charityproject_crud.remove(project_id,
                                                 session)
    return current_project