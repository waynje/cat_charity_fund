from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_name_duplicate, check_project_exists,
    check_correct_amount_to_update, check_project_was_invested_before_patch,
    check_project_was_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import make_investment, get_not_closed_projects
from app.models import Donation

router = APIRouter()


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):

    return await charityproject_crud.get_multiple(session)


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
    not_invested_donations = await get_not_closed_projects(session, Donation)
    make_investment(new_project, not_invested_donations)
    await session.commit()
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
    await check_project_was_invested_before_patch(current_project,
                                                  session)
    if obj_in.full_amount is not None:
        await check_correct_amount_to_update(project_id,
                                             session,
                                             obj_in.full_amount)
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name,
                                           session)
    return await charityproject_crud.update(current_project,
                                            obj_in,
                                            session)


@router.delete('/{project_id}',
               dependencies=[Depends(current_superuser)],
               response_model=CharityProjectDB)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):

    current_project = await check_project_exists(project_id,
                                                 session)
    await check_project_was_invested(current_project,
                                     session)
    return await charityproject_crud.remove(current_project,
                                            session)
