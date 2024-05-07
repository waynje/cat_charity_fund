from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_closed_projects(
    session: AsyncSession
):

    projects_to_invest = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == 0
    ).order_by('create_date'))
    project = projects_to_invest.scalars().first()

    donations = await session.execute(select(Donation).where(
        Donation.fully_invested == 0
    ).order_by('create_date'))
    donation = donations.scalars().first()

    return project, donation


async def make_investment(
    session: AsyncSession,
    obj
):

    project, donation = await get_not_closed_projects(session=session)
    project_balance = project.full_amount - project.invested_amount
    donation_balance = donation.full_amount - donation.invested_amount

    if project_balance > donation_balance:
        project.invested_amount += donation_balance
        donation.invested_amount += donation_balance
        donation.fully_invested = True
        donation.close_date = datetime.now()
    elif project_balance == donation_balance:
        project.invested_amount += donation_balance
        donation.invested_amount += donation_balance
        project.fully_invested = True
        donation.fully_invested = True
        project.close_date = datetime.now()
        donation.close_date = datetime.now()
    else:
        project.invested_amount += project_balance
        donation.invested_amount += project_balance
        project.fully_invested = True
        project.close_date = datetime.now()
    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)
    return await make_investment(session, obj)