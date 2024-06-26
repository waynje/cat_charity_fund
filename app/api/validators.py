from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import PositiveInt

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject


async def check_project_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:

    project_id = await (
        charityproject_crud.get_charity_project_id_by_name(
            project_name=project_name, session=session
        )
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким названием уже существует.'
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:

    project = await (charityproject_crud.get_charity_project(
        object_id=project_id,
        session=session))
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Такого проекта не существует.'
        )

    return project


async def check_project_closed(
    project_id: int,
    session: AsyncSession
):

    project_close_date = await (
        charityproject_crud.get_charity_project_close_date(
            project_id, session
        )
    )
    if project_close_date:
        return HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Данный проект был закрыт.'
        )


async def check_project_was_invested(
        charity_project: CharityProject,
        session: AsyncSession
) -> None:
    if charity_project.invested_amount > 0 or charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Нельзя удалять закрытый проект или проект,'
                    'в который уже были инвестированы средства')
        )


async def check_correct_amount_to_update(
    project_id: int,
    session: AsyncSession,
    full_amount_to_update: PositiveInt
):

    invested_amount = await (
        charityproject_crud.get_charity_project_invested_amount(
            project_id, session
        )
    )

    if invested_amount > full_amount_to_update:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Сумма донатов больше запрашиваемой. Изменить невозможно.'
        )


async def check_project_was_invested_before_patch(
        charity_project: CharityProject,
        session: AsyncSession
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Нельзя редактировать закрытый проект или проект,'
                    'в который уже были полностью инвестированы средства')
        )