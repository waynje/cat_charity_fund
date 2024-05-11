from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User, CharityProject
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investment import get_not_closed_projects, make_investment


router = APIRouter()


@router.get('/',
            response_model=List[DonationDB],
            dependencies=[Depends(current_superuser)],
            response_model_exclude_none=True)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multiple(session)


@router.get('/my',
            response_model=List[DonationDB],
            response_model_exclude=['user_id', 'invested_amount',
                                    'fully_invested', 'close_date'])
async def get_all_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_donations_by_user(session=session,
                                                     user=user)


@router.post('/',
             response_model=DonationDB,
             response_model_exclude=['user_id', 'invested_amount',
                                     'fully_invested', 'close_date'],
             response_model_exclude_none=True)
async def make_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation,
                                              session,
                                              user)
    not_invested_projects = await get_not_closed_projects(
        session,
        CharityProject)
    make_investment(new_donation, not_invested_projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation